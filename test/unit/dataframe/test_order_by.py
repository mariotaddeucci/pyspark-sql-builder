from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_order_by(spark: SparkSession) -> None:
    df = spark.table("users").orderBy(F.col("name").asc())
    assert df.generate_query() == (
        "SELECT * FROM (SELECT * FROM users) AS _t ORDER BY `name` ASC"
    )


def test_order_by_multiple(spark: SparkSession) -> None:
    df = spark.table("users").orderBy(F.col("age").desc(), F.col("name").asc())
    assert df.generate_query() == (
        "SELECT * FROM (SELECT * FROM users) AS _t ORDER BY `age` DESC, `name` ASC"
    )
