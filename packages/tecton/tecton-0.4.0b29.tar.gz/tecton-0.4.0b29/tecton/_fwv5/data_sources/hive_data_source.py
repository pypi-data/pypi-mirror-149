from typing import Callable
from typing import List
from typing import Optional

from tecton.data_sources.base_data_source_config import BaseBatchDSConfig
from tecton.data_sources.datetime_partition_column import DatetimePartitionColumn
from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_spark import function_serialization


class HiveConfig(BaseBatchDSConfig):
    """
    Configuration used to reference a Hive table.

    The HiveConfig class is used to create a reference to a Hive Table.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        table: str,
        database: str,
        timestamp_field: str = None,
        timestamp_format: str = None,
        skip_validation=False,
        datetime_partition_columns: List[DatetimePartitionColumn] = None,
        post_processor=None,
    ):
        """
        Instantiates a new HiveConfig.

        :param table: A table registered in Hive MetaStore.
        :param database: A database registered in Hive MetaStore.
        :param datetime_partition_columns: (Optional) List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param timestamp_field: Name of timestamp column.
        :param timestamp_format: (Optional) Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. See an example of
                                     post_processor in the `User Guide`_.

        :return: A HiveConfig class instance.

        .. _User Guide: https://docs.tecton.ai/v2/overviews/framework/data_sources.html

        Example of a HiveConfig declaration:

        .. code-block:: python

            from tecton import HiveConfig
            import pyspark

            def convert_temperature(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a HiveConfig instance, which can be used as a parameter to a BatchSource
            batch_config=HiveConfig(database='global_temperatures',
                                        table='us_cities',
                                        timestamp_field='timestamp',
                                        post_processor=convert_temperature)

        """
        self._args = prepare_hive_ds_args(
            table=table,
            database=database,
            timestamp_field=timestamp_field,
            timestamp_format=timestamp_format,
            datetime_partition_columns=datetime_partition_columns,
            post_processor=post_processor,
        )

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.hive_ds_config.CopyFrom(self._args)


def prepare_hive_ds_args(
    *,
    table: str,
    database: str,
    timestamp_field: Optional[str],
    timestamp_format: Optional[str],
    datetime_partition_columns: Optional[List[DatetimePartitionColumn]],
    post_processor: Optional[Callable],
):
    args = data_source_pb2.HiveDataSourceArgs()
    args.table = table
    args.database = database
    if timestamp_field:
        args.common_args.timestamp_field = timestamp_field
    if timestamp_format:
        args.timestamp_format = timestamp_format

    if datetime_partition_columns:
        for column in datetime_partition_columns:
            column_args = data_source_pb2.DatetimePartitionColumnArgs()
            column_args.column_name = column.column_name
            column_args.datepart = column.datepart
            column_args.zero_padded = column.zero_padded
            args.datetime_partition_columns.append(column_args)
    if post_processor is not None:
        args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))

    return args
