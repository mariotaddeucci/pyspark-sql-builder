from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_aggregate(spark: SparkSession) -> None:
    df = spark.table("sales").agg(
        F.count(F.col("id")).alias("num_orders"),
        F.sum(F.col("amount")).alias("total_amount"),
    )
    result = df.generate_query()
    assert "COUNT(`id`)" in result
    assert "SUM(`amount`)" in result
