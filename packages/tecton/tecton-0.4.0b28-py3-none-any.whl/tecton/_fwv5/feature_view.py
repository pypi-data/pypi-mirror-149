import datetime
import enum
import functools
from dataclasses import dataclass
from inspect import signature
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import attr
import pendulum
from google.protobuf.duration_pb2 import Duration
from pyspark.sql.types import StructType
from typeguard import typechecked

import tecton._fwv5 as fwv5
from tecton._fwv5.data_sources.request_data_source import RequestSource
from tecton._internals.fco import Fco
from tecton._internals.feature_definition import FeatureDefinition
from tecton._internals.feature_views.declarative_utils import FrameworkVersion
from tecton._internals.feature_views.declarative_utils import inputs_to_pipeline_nodes
from tecton._internals.feature_views.declarative_utils import test_binding_user_function
from tecton.aggregation_functions import AggregationFunction
from tecton.basic_info import prepare_basic_info
from tecton.data_sources.data_source import BaseDataSource
from tecton.data_sources.data_source import BatchDataSource
from tecton.data_sources.data_source import StreamDataSource
from tecton.data_sources.request_data_source import RequestDataSource
from tecton.entities.entity import Entity
from tecton.entities.entity import OverriddenEntity
from tecton.feature_services.feature_service_args import FeaturesConfig
from tecton.features_common.feature_configs import DatabricksClusterConfig
from tecton.features_common.feature_configs import DeltaConfig
from tecton.features_common.feature_configs import DynamoConfig
from tecton.features_common.feature_configs import EMRClusterConfig
from tecton.features_common.feature_configs import ExistingClusterConfig
from tecton.features_common.feature_configs import MonitoringConfig
from tecton.features_common.feature_configs import ParquetConfig
from tecton.features_common.feature_configs import RedisConfig
from tecton.features_common.inputs import _UnboundedInput
from tecton.features_common.inputs import Input
from tecton.transformations.transformation import Transformation
from tecton.transformations.transformation import transformation
from tecton.types import Field
from tecton.types import to_spark_schema_wrapper
from tecton_proto.args import feature_view_pb2
from tecton_proto.args.feature_view_pb2 import AggregationMode as AggregationModeProto
from tecton_proto.args.feature_view_pb2 import EntityKeyOverride
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.feature_view_pb2 import FeatureViewType
from tecton_proto.args.feature_view_pb2 import MaterializedFeatureViewArgs
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.virtual_data_source_pb2 import DataSourceType
from tecton_spark import logger as logger_lib
from tecton_spark.id_helper import IdHelper
from tecton_spark.materialization_context import BaseMaterializationContext
from tecton_spark.pipeline_common import transformation_type_checker
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


# This is the mode used when the feature view decorator is used on a pipeline function, i.e. one that only contains
# references to transformations and constants.
PIPELINE_MODE = "pipeline"

# This is used for the low latency streaming feature views.
CONTINUOUS_MODE = "continuous"

logger = logger_lib.get_logger("DeclarativeFeatureView")


# Create a parallel enum class since Python proto extensions do not use an enum class.
# Keep up-to-date with AggregationMode from tecton_proto/args/feature_view.proto.
class AggregationMode(enum.Enum):
    TIME_INTERVAL = AggregationModeProto.AGGREGATION_MODE_TIME_INTERVAL
    CONTINUOUS = AggregationModeProto.AGGREGATION_MODE_CONTINUOUS


@attr.s(auto_attribs=True)
class FeatureAggregation(object):
    """
    This class describes a single aggregation that is applied in a batch or stream window aggregate feature view.

    :param column: Column name of the feature we are aggregating.
    :type column: str
    :param function: One of the built-in aggregation functions.
    :type function: Union[str, AggregationFunction]
    :param time_windows: Duration to aggregate over. Examples: ``datetime.timedelta(days=30)``, ``[datetime.timedelta(hours=6), datetime.timedelta(days=1)]``.
    :type time_windows: Union[datetime.timedelta, List[datetime.timedelta]]

    `function` can be one of predefined numeric aggregation functions, namely ``"count"``, ``"sum"``, ``"mean"``, ``"min"``, ``"max"``. For
    these numeric aggregations, you can pass the name of it as a string. Nulls are handled like Spark SQL `Function(column)`, e.g. SUM/MEAN/MIN/MAX of all nulls is null and COUNT of all nulls is 0.

    In addition to numeric aggregations, :class:`FeatureAggregation` supports "last-n" aggregations that
    will compute the last N distinct values for the column by timestamp. Right now only string column types are supported as inputs
    to this aggregation, i.e., the resulting feature value will be a list of strings. Nulls are not included in the aggregated list.

    You can use it via the ``last_distinct()`` helper function like this:

    .. code-block:: python

        from tecton.aggregation_functions import last_distinct

        @batch_feature_view(
        ...
        aggregations=[FeatureAggregation(
            column='my_column',
            function=last_distinct(15),
            time_windows=[datetime.timedelta(days=7)])],
        ...
        )
        def my_fv(data_source):
            pass

    """

    column: str
    """Column name of the feature we are aggregating."""
    function: Union[str, AggregationFunction]
    """One of the built-in aggregation functions (`'count'`, `'sum'`, `'mean'`, `'min'`, `'max'`)."""
    time_windows: Union[datetime.timedelta, List[datetime.timedelta]]
    """
       Examples: ``datetime.timedelta(days=30)``, ``[datetime.timedelta(hours=6), datetime.timedelta(days=1)]``.
       """

    def _to_proto(self):
        proto = feature_view_pb2.FeatureAggregation()
        proto.column = self.column

        if isinstance(self.function, str):
            proto.function = self.function
        elif isinstance(self.function, AggregationFunction):
            proto.function = self.function.name
            for k, v in self.function.params.items():
                assert isinstance(v, int)
                proto.function_params[k].CopyFrom(feature_view_pb2.ParamValue(int64_value=v))
        else:
            raise TypeError(f"Invalid function type: {type(self.function)}")

        windows = self.time_windows if isinstance(self.time_windows, list) else [self.time_windows]
        for w in windows:
            duration = Duration()
            duration.FromTimedelta(w)
            proto.time_windows.append(duration)
        return proto


def get_source_input_params(user_function):
    # Filter out the materailization context to avoid mapping data sources to it.
    return [
        param.name
        for param in signature(user_function).parameters.values()
        if not isinstance(param.default, BaseMaterializationContext)
    ]


def prepare_common_fv_args(basic_info, entities, pipeline_function, inputs, fv_type) -> FeatureViewArgs:
    args = FeatureViewArgs()
    args.feature_view_type = fv_type
    args.feature_view_id.CopyFrom(IdHelper.from_string(IdHelper.generate_string_id()))

    args.framework_version = FrameworkVersion.FWV5.value
    args.version = FrameworkVersion.FWV5.value

    args.info.CopyFrom(basic_info)

    args.entities.extend([EntityKeyOverride(entity_id=entity._id(), join_keys=entity.join_keys) for entity in entities])

    inputs = inputs_to_pipeline_nodes(inputs)
    pipeline_fn_result = pipeline_function(**inputs)

    if fv_type == FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND:
        supported_modes = ["pipeline", "pandas", "python"]
    else:
        supported_modes = ["pipeline", "spark_sql", "snowflake_sql", "pyspark"]
    transformation_type_checker(basic_info.name, pipeline_fn_result, "pipeline", supported_modes)
    args.pipeline.root.CopyFrom(pipeline_fn_result)

    return args


class OnDemandFeatureView(FeatureDefinition):
    """
    OnDemandFeatureView internal declaration and testing class.

    **Do not instantiate this class directly.** Use :class:`tecton.on_demand_feature_view` instead.
    """

    def __init__(
        self,
        *,  # All arguments must be specified with keywords
        schema,
        transform,
        name: str,
        description: Optional[str],
        tags: Optional[Dict[str, str]],
        pipeline_function,
        owner: Optional[str],
        sources,
        user_function,
    ):
        """
        **Do not directly use this constructor.** Internal constructor for OnDemandFeatureView.

        :param schema: Spark schema declaring the expected output.
        :param transform: Transformation used to produce the feature values.
        :param name: Unique, human friendly name.
        :param description: Description.
        :param tags: Arbitrary key-value pairs of tagging metadata.
        :param pipeline_function: Pipeline definition function.
        :param owner: Owner name, used to organize features.
        :param sources: Sources passed into the pipeline.
        :param user_function: User-defined function.

        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)

        fn_params = get_source_input_params(user_function)
        inputs = {key: Input(value) for key, value in zip(fn_params, sources)}

        args = prepare_common_fv_args(
            basic_info=basic_info,
            entities=[],
            pipeline_function=pipeline_function,
            inputs=inputs,
            fv_type=FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND,
        )

        # We bind to user_function since pipeline_function may be artificially created and just accept **kwargs
        test_binding_user_function(user_function, inputs)

        if isinstance(schema, list):
            wrapper = to_spark_schema_wrapper(schema)
        else:
            wrapper = SparkSchemaWrapper(schema)
        args.on_demand_args.schema.CopyFrom(wrapper.to_proto())

        self._args = args
        self.inferred_transform = transform

        self.pipeline_function = pipeline_function
        self.schema = schema
        self.sources = sources

        Fco._register(self)


@typechecked
def on_demand_feature_view(
    *,
    mode: str,
    sources: List[Union[RequestDataSource, RequestSource, FeatureDefinition, FeaturesConfig]],
    schema: Union[StructType, List[Field]],
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    name: Optional[str] = None,
):
    """
    Declare an on-demand feature view

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: The sources passed into the pipeline. An Input can be a RequestDataSource or a materialized Feature View.
    :param output_schema: Spark schema matching the expected output (of either a dictionary or a Pandas DataFrame).
    :param description: Human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name override that identifies the FeatureView.
    :return: An object of type :class:`tecton.feature_views.OnDemandFeatureView`.

    An example declaration of an on-demand feature view using Python mode.
    With Python mode, the function sources will be dictionaries, and the function is expected to return a dictionary matching the schema from `output_schema`.
    Tecton recommends using Python mode for improved online serving performance.

    .. code-block:: python

        from tecton import RequestDataSource, Input, on_demand_feature_view
        from pyspark.sql.types import DoubleType, StructType, StructField, LongType

        request_schema = StructType([
            StructField('amount', DoubleType())
        ])
        transaction_request = RequestDataSource(request_schema=request_schema)

        output_schema = StructType([
            StructField('transaction_amount_is_high', LongType())
        ])


        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='python',
            output_schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production'},
            description='Whether the transaction amount is considered high (over $10000)'
        )
        def transaction_amount_is_high(transaction_request):

            result = {}
            result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
            return result

    An example declaration of an on-demand feature view using Pandas mode.
    With Pandas mode, the function sources will be Pandas Dataframes, and the function is expected to return a Dataframe matching the schema from `output_schema`.

    .. code-block:: python

        from tecton import RequestDataSource, Input, on_demand_feature_view
        from pyspark.sql.types import DoubleType, StructType, StructField, LongType
        import pandas

        # Define the request schema
        request_schema = StructType()
        request_schema.add(StructField('amount', DoubleType()))
        transaction_request = RequestDataSource(request_schema=request_schema)

        # Define the output schema
        output_schema = StructType()
        output_schema.add(StructField('transaction_amount_is_high', LongType()))

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high",
        # if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='pandas',
            output_schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production'},
            description='Whether the transaction amount is considered high (over $10000)'
        )
        def transaction_amount_is_high(transaction_request):
            import pandas as pd

            df = pd.DataFrame()
            df['transaction_amount_is_high'] = transaction_request['amount'] >= 10000).astype('int64')
            return df
    """

    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            transform = transformation(
                mode=mode, description=description, owner=owner, family=None, tags=tags, name_override=name
            )(user_function)

            def pipeline_function(**kwargs):
                return transform(**kwargs)

        feature_view = OnDemandFeatureView(
            schema=schema,
            transform=transform,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            sources=sources,
            description=description,
            owner=owner,
            tags=tags,
            user_function=user_function,
        )
        functools.update_wrapper(wrapper=feature_view, wrapped=user_function)

        return feature_view

    return decorator


@dataclass
class MaterializedFeatureView(FeatureDefinition):
    """
    Materialized FeatureView internal declaration and testing class.

    **Do not instantiate this class directly.** Use a decorator-based constructor instead:
        - :class:`tecton.batch_feature_view`
        - :class:`tecton.stream_feature_view`

    """

    def __init__(
        self,
        name: str,
        pipeline_function: Callable[..., PipelineNode],
        sources: Sequence[BaseDataSource],
        entities: List[Entity],
        online: bool,
        offline: bool,
        offline_store: Union[ParquetConfig, DeltaConfig],
        online_store: Optional[Union[DynamoConfig, RedisConfig]],
        aggregation_interval: Optional[datetime.timedelta],
        aggregations: Optional[List[FeatureAggregation]],
        ttl: Optional[datetime.timedelta],
        feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]],
        schedule_interval: Optional[datetime.timedelta],
        online_serving_index: Optional[List[str]],
        batch_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]],
        stream_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]],
        monitoring: Optional[MonitoringConfig],
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
        inferred_transform: Optional[Transformation],
        feature_view_type: FeatureViewType,
        timestamp_field: Optional[str],
        data_source_type: DataSourceType,
        user_function: Callable,
        is_custom: bool = False,
        aggregation_mode: Optional[AggregationMode] = None,
        max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    ):
        """
        **Do not directly use this constructor.** Internal constructor for materialized FeatureViews.
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)

        fn_params = get_source_input_params(user_function)
        if is_custom:
            inputs = {key: _UnboundedInput(value) for key, value in zip(fn_params, sources)}
        else:
            inputs = {key: Input(value) for key, value in zip(fn_params, sources)}

        args = prepare_common_fv_args(
            basic_info,
            entities,
            pipeline_function,
            inputs,
            fv_type=feature_view_type,
        )
        # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
        test_binding_user_function(user_function, inputs)

        if online_serving_index:
            args.online_serving_index.extend(online_serving_index)

        args.online_enabled = online
        args.offline_enabled = offline
        args.materialized_feature_view_args.CopyFrom(
            self._prepare_common_materialization_args(
                args.materialized_feature_view_args,
                timestamp_field,
                feature_start_time,
                schedule_interval,
                offline_store,
                online_store,
                batch_compute,
                stream_compute,
                monitoring,
                data_source_type,
                max_batch_aggregation_interval,
                is_custom=is_custom,
            )
        )
        args.materialized_feature_view_args.is_custom = is_custom
        if ttl:
            args.materialized_feature_view_args.serving_ttl.FromTimedelta(ttl)

        if aggregations:
            assert (
                aggregation_interval or aggregation_mode == AggregationMode.CONTINUOUS
            ), "`aggregation_interval` or `aggregation_mode=AggregationMode.CONTINUOUS` is required if specifying aggregations"
            assert ttl is None, "`ttl` is automatically set for aggregations to the `aggregation_interval`"

            if aggregation_mode == AggregationMode.CONTINUOUS:
                args.materialized_feature_view_args.aggregation_interval.FromTimedelta(datetime.timedelta(seconds=0))
            if aggregation_mode == AggregationMode.TIME_INTERVAL:
                args.materialized_feature_view_args.aggregation_interval.FromTimedelta(aggregation_interval)

            args.materialized_feature_view_args.aggregation_mode = aggregation_mode.value
            args.materialized_feature_view_args.aggregations.extend([agg._to_proto() for agg in aggregations])
            args.materialized_feature_view_args.aggregation_mode = aggregation_mode.value
        else:
            assert (
                aggregation_interval is None
            ), "`aggregation_interval` can only be specified when using `aggregations`"
            assert aggregation_mode is None, "`aggregation_mode` can only be specified when using `aggregations`"

            # Default ttl to "infinity" equivalent
            ttl = ttl or datetime.timedelta.max

        self.inferred_transform = inferred_transform
        self._args = args
        self.pipeline_function = pipeline_function
        self.sources = sources

        Fco._register(self)

    def _prepare_common_materialization_args(
        self,
        args: MaterializedFeatureViewArgs,
        timestamp_field: Optional[str],
        feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]],
        schedule_interval: Optional[datetime.timedelta],
        offline_store: Union[ParquetConfig, DeltaConfig],
        online_store: Optional[Union[DynamoConfig, RedisConfig]],
        batch_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]],
        stream_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]],
        monitoring: Optional[MonitoringConfig],
        data_source_type: DataSourceType,
        max_batch_aggregation_interval: Optional[datetime.timedelta],
        is_custom: bool,
    ) -> MaterializedFeatureViewArgs:
        if timestamp_field:
            args.timestamp_field = timestamp_field

        if feature_start_time:
            args.feature_start_time.FromDatetime(feature_start_time)
        if schedule_interval:
            args.schedule_interval.FromTimedelta(schedule_interval)
        args.offline_store.CopyFrom(offline_store._to_proto())
        if online_store:
            args.online_store.CopyFrom(online_store._to_proto())
        if batch_compute:
            cluster_config = batch_compute._to_cluster_proto()
            args.batch_compute.CopyFrom(cluster_config)
        if stream_compute:
            cluster_config = stream_compute._to_cluster_proto()
            args.stream_compute.CopyFrom(cluster_config)

        if max_batch_aggregation_interval:
            args.max_batch_aggregation_interval.FromTimedelta(max_batch_aggregation_interval)

        if monitoring:
            args.monitoring.CopyFrom(monitoring._to_proto())
        if data_source_type:
            args.data_source_type = data_source_type

        args.is_custom = is_custom

        return args

    def __hash__(self):
        return self.name.__hash__()


# TODO(convergence): SDK documentation
@typechecked
def stream_feature_view(
    *,
    mode: str,
    source: Union[StreamDataSource, fwv5.StreamSource],
    entities: List[Union[fwv5.Entity, Entity, OverriddenEntity]],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregation_mode: Optional[AggregationMode] = None,
    aggregations: List[FeatureAggregation] = [],
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
    schedule_interval: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[List[str]] = None,
    batch_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]] = None,
    stream_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]] = None,
    offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
    online_store: Optional[Union[DynamoConfig, RedisConfig]] = None,
    monitoring: Optional[MonitoringConfig] = None,
    description: str = "",
    owner: str = "",
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
):
    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = transformation(mode, name, description, owner, family=None, tags=tags)(user_function)

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        _aggregation_mode = aggregation_mode or AggregationMode.TIME_INTERVAL if aggregations else None

        featureView = MaterializedFeatureView(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            inferred_transform=inferred_transform,
            sources=[source],
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            aggregation_mode=_aggregation_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            schedule_interval=schedule_interval,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitoring=monitoring,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.STREAM_WITH_BATCH,
            user_function=user_function,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
        )
        functools.update_wrapper(featureView, user_function)

        return featureView

    return decorator


# TODO(convergence): SDK documentation
@typechecked
def batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[BatchDataSource, fwv5.BatchSource]],
    entities: List[Union[fwv5.Entity, Entity, OverriddenEntity]],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: List[FeatureAggregation] = [],
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
    schedule_interval: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[List[str]] = None,
    batch_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]] = None,
    offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
    online_store: Optional[Union[DynamoConfig, RedisConfig]] = None,
    monitoring: Optional[MonitoringConfig] = None,
    description: str = "",
    owner: str = "",
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
):
    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = transformation(mode, name, description, owner, family=None, tags=tags)(user_function)

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        aggregation_mode = AggregationMode.TIME_INTERVAL if aggregations else None

        featureView = MaterializedFeatureView(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            inferred_transform=inferred_transform,
            sources=sources,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            aggregation_mode=aggregation_mode,
            aggregations=aggregations,
            ttl=ttl,
            feature_start_time=feature_start_time,
            schedule_interval=schedule_interval,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitoring=monitoring,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.BATCH,
            user_function=user_function,
            max_batch_aggregation_interval=max_batch_aggregation_interval,
        )
        functools.update_wrapper(featureView, user_function)

        return featureView

    return decorator


# TODO(convergence): SDK documentation
@typechecked
def custom_batch_feature_view(
    *,
    mode: str,
    sources: Sequence[Union[BatchDataSource, fwv5.BatchSource]],
    entities: List[Union[fwv5.Entity, Entity, OverriddenEntity]],
    online: Optional[bool] = False,
    offline: Optional[bool] = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime.datetime]] = None,
    schedule_interval: Optional[datetime.timedelta] = None,
    batch_compute: Optional[Union[ExistingClusterConfig, DatabricksClusterConfig, EMRClusterConfig]] = None,
    offline_store: Optional[Union[ParquetConfig, DeltaConfig]] = ParquetConfig(),
    online_store: Optional[Union[DynamoConfig, RedisConfig]] = None,
    monitoring: Optional[MonitoringConfig] = None,
    description: str = "",
    owner: str = "",
    tags: Optional[Dict[str, str]] = None,
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
):
    def decorator(user_function):
        if mode == PIPELINE_MODE:
            pipeline_function = user_function
            inferred_transform = None
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = transformation(mode, name, description, owner, family=None, tags=tags)(user_function)

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        featureView = MaterializedFeatureView(
            feature_view_type=FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name or user_function.__name__,
            pipeline_function=pipeline_function,
            inferred_transform=inferred_transform,
            sources=sources,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=None,
            aggregations=None,
            ttl=ttl,
            feature_start_time=feature_start_time,
            schedule_interval=schedule_interval,
            online_serving_index=None,
            batch_compute=batch_compute,
            stream_compute=None,
            monitoring=monitoring,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=DataSourceType.BATCH,
            user_function=user_function,
            is_custom=True,
        )
        functools.update_wrapper(featureView, user_function)

        return featureView

    return decorator
