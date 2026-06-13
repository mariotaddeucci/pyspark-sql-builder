from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_with_column(spark: SparkSession) -> None:
    df = (
        spark.table("users")
        .select("id", "price")
        .withColumn("total", F.col("price") * F.lit(1.1))
    )
    result = df.generate_query()
    assert "total" in result
