from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_copy(spark: SparkSession) -> None:
    df1 = spark.table("users").select("id", "name")
    df2 = df1.copy()
    assert df1.generate_query() == df2.generate_query()
