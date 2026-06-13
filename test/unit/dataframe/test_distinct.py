from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_distinct(spark: SparkSession) -> None:
    df = spark.table("users").select("city").distinct()
    assert df.generate_query() == (
        "SELECT DISTINCT * FROM (SELECT `city` FROM users) AS _t"
    )
