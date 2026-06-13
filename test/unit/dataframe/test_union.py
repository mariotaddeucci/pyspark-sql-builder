from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_union_all(spark: SparkSession) -> None:
    df1 = spark.table("users_2023")
    df2 = spark.table("users_2024")
    result = df1.unionAll(df2)
    assert "UNION ALL" in result.generate_query()
