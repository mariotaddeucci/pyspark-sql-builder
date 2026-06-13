from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_select_all(spark: SparkSession) -> None:
    df = spark.table("users")
    assert df.generate_query() == "SELECT * FROM users"


def test_select_columns(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    assert df.generate_query() == "SELECT `id`, `name` FROM users"


def test_select_column_objects(spark: SparkSession) -> None:
    df = spark.table("users").select(F.col("id"), F.col("name"))
    assert df.generate_query() == "SELECT `id`, `name` FROM users"
