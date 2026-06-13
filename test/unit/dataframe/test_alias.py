from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_alias(spark: SparkSession) -> None:
    df = spark.table("users").alias("u")
    assert df.generate_query() == "SELECT * FROM (SELECT * FROM users) AS u"
