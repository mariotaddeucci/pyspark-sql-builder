from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_limit(spark: SparkSession) -> None:
    df = spark.table("users").limit(10)
    assert df.generate_query() == ("SELECT * FROM (SELECT * FROM users) AS _t LIMIT 10")
