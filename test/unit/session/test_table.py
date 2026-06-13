from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_table(spark: SparkSession) -> None:
    df = spark.table("users")
    assert df.generate_query() == "SELECT * FROM users"
