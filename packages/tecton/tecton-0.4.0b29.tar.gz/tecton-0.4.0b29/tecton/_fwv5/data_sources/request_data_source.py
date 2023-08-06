from typing import List

from tecton.types import Field
from tecton_spark.id_helper import IdHelper


class RequestSource:
    """
    Declare a ``RequestSource``, for using request-time data in an ``OnDemandFeatureView``.
    """

    def __init__(
        self,
        schema: List[Field],
    ):
        """
        Creates a new RequestSource

        :param request_schema: PySpark schema for the RequestSource inputs.

        Example of a RequestSource declaration:

        .. code-block:: python

            from tecton import RequestSource
            from tecton.types import Field, DataType

            schema = [Field('amount', DataType.FLOAT64)]
            transaction_request = RequestSource(schema=schema)
        """
        self.schema = schema
        self.id = IdHelper.from_string(IdHelper.generate_string_id())
