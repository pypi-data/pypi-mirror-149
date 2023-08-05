import datetime
from typing import Dict
from typing import List
from typing import Optional

from tecton.data_sources.base_data_source_config import BaseStreamDSConfig
from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_spark import data_source_helper
from tecton_spark import function_serialization


class KinesisConfig(BaseStreamDSConfig):
    """
    Configuration used to reference a Kinesis stream.

    The KinesisConfig class is used to create a reference to an AWS Kinesis stream.

    This class used as an input to a :class:`StreamSource`'s parameter ``stream_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``StreamSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        stream_name: str,
        region: str,
        post_processor,
        timestamp_field: str,
        initial_stream_position: str,
        watermark_delay_threshold: datetime.timedelta,
        deduplication_columns: List[str] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Instantiates a new KinesisConfig.

        :param stream_name: Name of the Kinesis stream.
        :param region: AWS region of the stream, e.g: "us-west-2".
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the `User Guide`_.
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param initial_stream_position: Initial position in stream, e.g: "latest" or "trim_horizon".
                                                More information available in `Spark Kinesis Documentation`_.
        :param watermark_delay_threshold: Watermark time interval, e.g: timedelta(hours=24), used by Spark Structured Streaming to account for late-arriving data. See: https://docs.tecton.ai/v2/overviews/framework/feature_views/stream_feature_view.html#productionizing-a-stream
        :param deduplication_columns: (Optional) Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating.
        :param options: (Optional) A map of additional Spark readStream options

        :return: A KinesisConfig class instance.

        .. _User Guide: https://docs.tecton.ai/v2/overviews/framework/data_sources.html
        .. _Spark Kinesis Documentation: https://spark.apache.org/docs/latest/streaming-kinesis-integration.html

        Example of a KinesisConfig declaration:

        .. code-block:: python

            import pyspark
            from tecton import KinesisConfig


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
            # Declare KinesisConfig instance object that can be used as argument in `StreamSource`
            stream_config = KinesisConfig(
                                    stream_name='transaction_events',
                                    region='us-west-2',
                                    initial_stream_position='latest',
                                    watermark_delay_threshold=timedelta(minutes=30),
                                    timestamp_field='timestamp',
                                    post_processor=raw_data_deserialization,
                                    options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
            )
        """

        self._args = prepare_kinesis_ds_args(
            stream_name=stream_name,
            region=region,
            post_processor=post_processor,
            timestamp_field=timestamp_field,
            initial_stream_position=initial_stream_position,
            watermark_delay_threshold=watermark_delay_threshold,
            deduplication_columns=deduplication_columns,
            options=options,
        )

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kinesis_ds_config.CopyFrom(self._args)


def prepare_kinesis_ds_args(
    *,
    stream_name: str,
    region: str,
    post_processor,
    timestamp_field: str,
    initial_stream_position: Optional[str],
    watermark_delay_threshold: Optional[datetime.timedelta],
    deduplication_columns: Optional[List[str]],
    options: Optional[Dict[str, str]],
):
    args = data_source_pb2.KinesisDataSourceArgs()
    args.stream_name = stream_name
    args.region = region
    args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
    args.common_args.timestamp_field = timestamp_field
    if initial_stream_position:
        args.initial_stream_position = data_source_helper.INITIAL_STREAM_POSITION_STR_TO_ENUM[initial_stream_position]
    if watermark_delay_threshold:
        args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
    if deduplication_columns:
        for column_name in deduplication_columns:
            args.deduplication_columns.append(column_name)
    options_ = options or {}
    for key in sorted(options_.keys()):
        option = data_source_pb2.Option()
        option.key = key
        option.value = options_[key]
        args.options.append(option)

    return args
