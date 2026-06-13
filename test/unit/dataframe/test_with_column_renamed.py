from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_with_column_renamed(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    df = df.withColumnRenamed("name", "username")
    result = df.generate_query()
    assert "username" in result
