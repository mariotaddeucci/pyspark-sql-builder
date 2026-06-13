from __future__ import annotations

from pyspark_sql_builder.readwriter import DataFrameReader
from pyspark_sql_builder.session import SparkSession


def test_read_property(spark: SparkSession) -> None:
    assert isinstance(spark.read, DataFrameReader)


def test_read_table(spark: SparkSession) -> None:
    df = spark.read.table("users")
    assert df.generate_query() == "SELECT * FROM users"
