from collections.abc import Callable
from typing import Optional

from pyspark.sql.types import StructType

from tecton.data_sources.base_data_source_config import BaseBatchDSConfig
from tecton_proto.args.data_source_pb2 import FileDataSourceArgs
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_spark import function_serialization
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


class FileConfig(BaseBatchDSConfig):
    """
    Configuration used to reference a file or directory (S3, etc.)

    The FileConfig class is used to create a reference to a file or directory of files in S3,
    HDFS, or DBFS.

    The schema of the data source is inferred from the underlying file(s). It can also be modified using the
    ``post_processor`` parameter.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare a part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        uri: str,
        file_format: str,
        convert_to_glue_format=False,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        schema_uri: Optional[str] = None,
        schema_override: Optional[StructType] = None,
    ):
        """
        Instantiates a new FileConfig.

        :param uri: S3 or HDFS path to file(s).
        :param file_format: File format. "json", "parquet", or "csv"
        :param convert_to_glue_format: Converts all schema column names to lowercase.
        :param timestamp_field: Name of timestamp column.
        :param timestamp_format: (Optional) Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     Pyspark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. See an example of
                                     post_processor in the `User Guide`_.
        :param schema_uri: (Optional) A file or subpath of "uri" that can be used for fast schema inference.
                           This is useful for speeding up plan computation for highly partitioned data sources containing many files.
        :param schema_override: (Optional) a pyspark.sql.types.StructType object that will be used as the schema when
                                reading from the file. If omitted, the schema will be inferred automatically.

        :return: A FileConfig class instance.

        .. _User Guide: https://docs.tecton.ai/v2/overviews/framework/data_sources.html

        Example of a FileConfig declaration:

        .. code-block:: python

            from tecton import FileConfig, BatchSource

            def convert_temperature(df):
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a FileConfig, which can be used as a parameter to a `BatchSource`
            ad_impressions_file_ds = FileConfig(uri="s3://tecton.ai.public/data/ad_impressions_sample.parquet",
                                                file_format="parquet",
                                                timestamp_field="timestamp",
                                                post_processor=convert_temperature)

            # This FileConfig can then be included as an parameter a BatchSource declaration.
            # For example,
            ad_impressions_batch = BatchSource(name="ad_impressions_batch",
                                                   batch_config=ad_impressions_file_ds)

        """
        self._args = prepare_file_ds_args(
            uri=uri,
            file_format=file_format,
            convert_to_glue_format=convert_to_glue_format,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            post_processor=post_processor,
            schema_uri=schema_uri,
            schema_override=schema_override,
        )

    def _merge_batch_args(self, data_source_args: VirtualDataSourceArgs):
        data_source_args.file_ds_config.CopyFrom(self._args)


def prepare_file_ds_args(
    *,
    uri: str,
    file_format: str,
    convert_to_glue_format: bool,
    timestamp_field: Optional[str],
    timestamp_format: Optional[str],
    post_processor: Optional[Callable],
    schema_uri: Optional[str],
    schema_override: Optional[StructType],
) -> FileDataSourceArgs:
    args = FileDataSourceArgs()
    args.uri = uri
    args.file_format = file_format
    args.convert_to_glue_format = convert_to_glue_format
    if schema_uri is not None:
        args.schema_uri = schema_uri
    if post_processor is not None:
        args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
    if timestamp_field:
        args.common_args.timestamp_field = timestamp_field
    if timestamp_format:
        args.timestamp_format = timestamp_format
    if schema_override:
        args.schema_override.CopyFrom(SparkSchemaWrapper(schema_override).to_proto())

    return args
