from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_range(spark: SparkSession) -> None:
    df = spark.range(0, 10)
    assert "range" in df.generate_query().lower()
