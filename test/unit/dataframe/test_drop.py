from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_drop(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name", "age").drop("age")
    result = df.generate_query()
    assert "id" in result
    assert "name" in result
    assert "EXCLUDE" in result
