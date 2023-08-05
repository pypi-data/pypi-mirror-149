from typing import Dict
from typing import Optional
from typing import Union

from typeguard import typechecked

from tecton._fwv5.data_sources.file_data_source import FileConfig
from tecton._fwv5.data_sources.hive_data_source import HiveConfig
from tecton._fwv5.data_sources.kafka_data_source import KafkaConfig
from tecton._fwv5.data_sources.kinesis_data_source import KinesisConfig
from tecton._fwv5.data_sources.redshift_data_source import RedshiftConfig
from tecton._fwv5.data_sources.snowflake_data_source import SnowflakeConfig
from tecton._internals.fco import Fco
from tecton.basic_info import prepare_basic_info
from tecton.data_sources.base_data_source_config import BaseBatchDSConfig
from tecton.data_sources.base_data_source_config import BaseStreamDSConfig
from tecton.data_sources.data_source import BaseDataSource
from tecton_proto.args import virtual_data_source_pb2
from tecton_proto.args.basic_info_pb2 import BasicInfo
from tecton_proto.args.repo_metadata_pb2 import SourceInfo
from tecton_proto.args.version_constraints_pb2 import FrameworkVersion
from tecton_proto.args.virtual_data_source_pb2 import DataSourceType
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_spark.id_helper import IdHelper
from tecton_spark.logger import get_logger

logger = get_logger("DataSource")


class FWv4BaseDataSource(BaseDataSource):
    @property
    def timestamp_field(self) -> str:
        """
        The name of the timestamp column or key of this DataSource.
        """
        if self._args.HasField("hive_ds_config"):
            return self._args.hive_ds_config.timestamp_field
        if self._args.HasField("redshift_ds_config"):
            return self._args.redshift_ds_config.timestamp_field
        if self._args.HasField("snowflake_ds_config"):
            return self._args.snowflake_ds_config.timestamp_field
        if self._args.HasField("file_ds_config"):
            return self._args.file_ds_config.timestamp_field
        else:
            raise Exception(f"Unknown Data Source Type: {self.name}")


class BatchSource(FWv4BaseDataSource):
    """
    Declare a ``BatchSource``, used to read batch data into Tecton.

    ``BatchFeatureViews`` and ``BatchWindowAggregateFeatureViews`` ingest data from a BatchSource.
    """

    _args: VirtualDataSourceArgs
    _source_info: SourceInfo

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        tags: Dict[str, str] = None,
        owner: str = "",
        batch_config: Union[FileConfig, HiveConfig, RedshiftConfig, SnowflakeConfig],
    ) -> None:
        """
        Creates a new BatchSource

        :param name: An unique name of the DataSource.
        :param description: (Optional) Description.
        :param tags: (Optional) Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param batch_config: BatchConfig object containing the configuration of the batch data source to be included
            in this DataSource.

        :return: A :class:`BatchSource` class instance.

        Example of a BatchSource declaration:

        .. code-block:: python

            from tecton import HiveConfig

            # Declare a BatchSource with HiveConfig instance as its batch_config parameter
            # Refer to Configs API documentation other batch_config types.
            credit_scores_batch = BatchSource(name='credit_scores_batch',
                                                  batch_config=HiveConfig(
                                                        database='demo_fraud',
                                                        table='credit_scores',
                                                        timestamp_field='timestamp'),
                                                  owner='matt@tecton.ai',
                                                  tags={'release': 'staging',
                                                        'source: 'nexus'})
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)
        args = prepare_ds_args(
            basic_info=basic_info, batch_config=batch_config, stream_config=None, ds_type=DataSourceType.BATCH
        )

        self._args = args

        Fco._register(self)


class StreamSource(FWv4BaseDataSource):
    """
    Declare a ``StreamSource``, used to read streaming data into Tecton.

    ``StreamFeatureViews`` and ``StreamWindowAggregateFeatureViews`` ingest data from StreamSources.
    A StreamSource contains both a batch and a stream data source configs.
    """

    _args: VirtualDataSourceArgs
    _source_info: SourceInfo

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        tags: Dict[str, str] = None,
        owner: str = "",
        batch_config: Union[FileConfig, HiveConfig, RedshiftConfig, SnowflakeConfig],
        stream_config: Union[KinesisConfig, KafkaConfig],
    ) -> None:
        # TODO: docstring
        """
        Creates a new StreamSource.

        :param name: An unique name of the DataSource.
        :param description: (Optional) Description.
        :param tags: (Optional) Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param batch_config: BatchConfig object containing the configuration of the batch data source that is to be included
            in this DataSource.
        :param stream_config: StreamConfig object containing the configuration of the
            stream data source that is to be included in this DataSource.

        :return: A :class:`StreamSource` class instance.

        Example of a StreamSource declaration:

        .. code-block:: python

         import pyspark
            from tecton import KinesisConfig, HiveConfig


            # Define our deserialization raw stream translator
            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import col, from_json, from_utc_timestamp
                from pyspark.sql.types import StructType, StringType

                payload_schema = (
                  StructType()
                        .add('amount', StringType(), False)
                        .add('isFraud', StringType(), False)
                        .add('timestamp', StringType(), False)
                )
                return (
                    df.selectExpr('cast (data as STRING) jsonData')
                    .select(from_json('jsonData', payload_schema).alias('payload'))
                    .select(
                        col('payload.amount').cast('long').alias('amount'),
                        col('payload.isFraud').cast('long').alias('isFraud'),
                        from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                    )
                )

            # Declare a StreamSource with both a batch_config and a stream_config as parameters
            # See the API documentation for both BatchConfig and StreamConfig
            transactions_stream = StreamSource(
                                    name='transactions_stream',
                                    stream_config=KinesisConfig(
                                        stream_name='transaction_events',
                                        region='us-west-2',
                                        initial_stream_position='latest',
                                        watermark_delay_threshold='30 minutes',
                                        timestamp_field='timestamp',
                                        post_processor=raw_data_deserialization,
                                        options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
                                    ),
                                    batch_config=HiveConfig(
                                        database='demo_fraud',
                                        table='transactions',
                                        timestamp_field='timestamp',
                                    ),
                                    owner='jules@tecton.ai',
                                    tags={'release': 'staging',
                                          'source: 'mobile'})
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)
        args = prepare_ds_args(
            basic_info=basic_info,
            batch_config=batch_config,
            stream_config=stream_config,
            ds_type=DataSourceType.STREAM_WITH_BATCH,
        )

        self._args = args

        Fco._register(self)


def prepare_ds_args(
    *,
    basic_info: BasicInfo,
    batch_config: BaseBatchDSConfig,
    stream_config: Optional[BaseStreamDSConfig],
    ds_type: Optional["DataSourceType"],
):
    args = virtual_data_source_pb2.VirtualDataSourceArgs()
    args.virtual_data_source_id.CopyFrom(IdHelper.from_string(IdHelper.generate_string_id()))
    args.info.CopyFrom(basic_info)
    args.version = FrameworkVersion.FWV5
    batch_config._merge_batch_args(args)
    if stream_config is not None:
        stream_config._merge_stream_args(args)
    if ds_type:
        args.type = ds_type
    return args
