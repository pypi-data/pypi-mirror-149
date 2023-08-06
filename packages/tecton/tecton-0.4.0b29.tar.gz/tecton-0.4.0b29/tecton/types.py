from collections import namedtuple
from enum import Enum
from typing import List

from pyspark.sql.types import BooleanType
from pyspark.sql.types import ByteType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from typeguard import typechecked

from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


class DataType(namedtuple("DataType", ["name", "spark_type"]), Enum):
    INT32 = "int32", LongType()
    INT64 = "int64", LongType()
    FLOAT32 = "float32", DoubleType()
    FLOAT64 = "float64", DoubleType()
    STRING = "string", StringType()
    BYTES = "bytes", ByteType()
    BOOL = "bool", BooleanType()
    # Array type is not supported yet.


@typechecked
class Field:
    def __init__(
        self,
        name: str,
        dataType: DataType,
    ):
        self.name = name
        self.dataType = dataType

    def to_spark_struct_field(self) -> StructField:
        return StructField(self.name, self.dataType.spark_type)


def to_spark_schema_wrapper(field_list: List[Field]) -> SparkSchemaWrapper:
    s = StructType([field.to_spark_struct_field() for field in field_list])
    return SparkSchemaWrapper(s)
