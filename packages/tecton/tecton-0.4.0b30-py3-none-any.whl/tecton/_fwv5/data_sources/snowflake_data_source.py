from typing import Optional

from tecton.data_sources.base_data_source_config import BaseBatchDSConfig
from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_spark import function_serialization


class SnowflakeConfig(BaseBatchDSConfig):
    """
    Configuration used to reference a Snowflake table or query.

    The SnowflakeConfig class is used to create a reference to a Snowflake table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        *,
        database: str,
        schema: str,
        warehouse: Optional[str] = None,
        url: Optional[str] = None,
        role: Optional[str] = None,
        table: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        post_processor=None,
    ):
        """
        Instantiates a new SnowflakeConfig. One of table and query should be specified when creating this file.

        :param url: The connection URL to Snowflake, which contains account information
                         (e.g. https://xy12345.eu-west-1.snowflakecomputing.com).
        :param database: The Snowflake database for this Data source.
        :param schema: The Snowflake schema for this Data source.
        :param warehouse: The Snowflake warehouse for this Data source.
        :param role: (Optional) The Snowflake role that should be used for this Data source.

        :param table: The table for this Data source. Only one of `table` and `query` must be specified.
        :param query: The query for this Data source. Only one of `table` and `query` must be specified.

        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. See an example of
                                     post_processor in the `User Guide`_.
        :param timestamp_field: (Optional) The name of the timestamp column (after the post_processor has been applied).
                               The column name does not need to be specified if there is exactly one timestamp column after the translator is applied.
                               This is needed for efficient time filtering when materializing batch features.

        :return: A SnowflakeConfig class instance.

        .. _User Guide: https://docs.tecton.ai/v2/overviews/framework/data_sources.html

        Example of a SnowflakeConfig declaration:

        .. code-block:: python

            from tecton import SnowflakeConfig, BatchSource

            # Declare SnowflakeConfig instance object that can be used as an argument in BatchSource
            snowflake_ds_config = SnowflakeConfig(
                                              url="https://<your-cluster>.eu-west-1.snowflakecomputing.com/",
                                              database="CLICK_STREAM_DB",
                                              schema="CLICK_STREAM_SCHEMA",
                                              warehouse="COMPUTE_WH",
                                              table="CLICK_STREAM_FEATURES",
                                              query="SELECT timestamp as ts, created, user_id, clicks, click_rate"
                                                     "FROM CLICK_STREAM_DB.CLICK_STREAM_FEATURES")

            # Use in the BatchSource
            snowflake_ds = BatchSource(name="click_stream_snowflake_ds",
                                           batch_config=snowflake_ds_config)
        """
        self._args = args = data_source_pb2.SnowflakeDataSourceArgs()
        args.database = database
        args.schema = schema
        if url:
            args.url = url
        if warehouse:
            args.warehouse = warehouse

        if role:
            args.role = role

        if table:
            args.table = table
        if query:
            args.query = query

        if post_processor is not None:
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.snowflake_ds_config.CopyFrom(self._args)
