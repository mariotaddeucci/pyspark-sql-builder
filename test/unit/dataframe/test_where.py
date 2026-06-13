from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_where_condition(spark: SparkSession) -> None:
    df = spark.table("users").where(F.col("age") > 18)
    assert df.generate_query() == (
        "SELECT * FROM (SELECT * FROM users) AS _t WHERE `age` > 18"
    )


def test_multiple_where(spark: SparkSession) -> None:
    df = (
        spark.table("users").where(F.col("age") > 18).where(F.col("status") == "active")
    )
    expected = (
        "SELECT * FROM (SELECT * FROM (SELECT * FROM users)"
        " AS _t WHERE `age` > 18) AS _t WHERE `status` = 'active'"
    )
    assert df.generate_query() == expected


def test_select_with_where(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name", "age").where(F.col("age") >= 21)
    expected = (
        "SELECT * FROM (SELECT `id`, `name`, `age` FROM users) AS _t WHERE `age` >= 21"
    )
    assert df.generate_query() == expected
