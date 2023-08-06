from typing import Optional

from tecton.data_sources.base_data_source_config import BaseBatchDSConfig
from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_spark import function_serialization


class RedshiftConfig(BaseBatchDSConfig):
    """
    Configuration used to reference a Redshift table or query.

    The RedshiftConfig class is used to create a reference to a Redshift table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        endpoint: str,
        table: Optional[str] = None,
        post_processor=None,
        temp_s3: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
    ):
        """
        Instantiates a new RedshiftConfig. One of table and query should be specified when creating this file.

        :param endpoint: The connection endpoint to Redshift
                         (e.g. redshift-cluster-1.cigcwzsdltjs.us-west-2.redshift.amazonaws.com:5439/dev).
        :param table: The Redshift table for this Data source. Only one of table and query should be specified.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. See an example of
                                     post_processor in the `User Guide`_.
        :param query: A Redshift query for this Data source. Only one of table and query should be specified.
        :param temp_s3: [deprecated] An S3 URI destination for intermediate data that is needed for Redshift.
                        (e.g. s3://tecton-ai-test-cluster-redshift-data)
        :param timestamp_field: (Optional) The name of the timestamp column (after the post_processor has been applied).
                               The column name does not need to be specified if there is exactly one timestamp column after the translator is applied.
                               This is needed for efficient time filtering when materializing batch features.

        :return: A RedshiftConfig class instance.

        .. _User Guide: https://docs.tecton.ai/v2/overviews/framework/data_sources.html

        Example of a RedshiftConfig declaration:

        .. code-block:: python

            from tecton import RedshiftConfig

            # Declare RedshiftConfig instance object that can be used as an argument in BatchSource
            redshift_ds_config = RedshiftConfig(endpoint="cluster-1.us-west-2.redshift.amazonaws.com:5439/dev",
                                                  table="ad_serving_features",
                                                  query="SELECT timestamp as ts, created, user_id, ad_id, duration"
                                                        "FROM ad_serving_features")
        """
        self._args = args = data_source_pb2.RedshiftDataSourceArgs()
        args.endpoint = endpoint

        if table and query:
            raise AssertionError(f"Should only specify one of table and query sources for redshift")
        if not table and not query:
            raise AssertionError(f"Missing both table and query sources for redshift, exactly one must be present")

        if table:
            args.table = table
        else:
            args.query = query

        if post_processor is not None:
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.redshift_ds_config.CopyFrom(self._args)
