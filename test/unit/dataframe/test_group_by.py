from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


def test_group_by_agg(spark: SparkSession) -> None:
    df = spark.table("sales").select(
        F.col("category"), F.sum(F.col("amount")).alias("total")
    )
    grouped = df.groupBy("category")
    assert grouped is not None


def test_group_by_having_agg(spark: SparkSession) -> None:
    df = (
        spark.table("sales")
        .select(F.col("category"), F.sum(F.col("amount")).alias("total"))
        .having(F.sum(F.col("amount")) > 1000)
    )
    result = df.generate_query()
    assert "HAVING" in result
