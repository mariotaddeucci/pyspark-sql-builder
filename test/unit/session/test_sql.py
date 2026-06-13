from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_sql_method(spark: SparkSession) -> None:
    df = spark.sql("SELECT id, name FROM users")
    assert df.generate_query() == "SELECT id, name FROM users"
