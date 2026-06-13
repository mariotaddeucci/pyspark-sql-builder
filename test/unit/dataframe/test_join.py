from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


def test_join_inner(spark: SparkSession) -> None:
    df = spark.table("orders").join(
        "customers", F.col("orders.customer_id") == F.col("customers.id")
    )
    result = df.generate_query()
    assert "JOIN customers" in result
    assert "`orders`.`customer_id` = `customers`.`id`" in result


def test_join_using(spark: SparkSession) -> None:
    df = spark.table("employees").join("departments", ["dept_id"])
    result = df.generate_query()
    assert "JOIN departments USING" in result
    assert "`dept_id`" in result


def test_join_using_multiple(spark: SparkSession) -> None:
    df = spark.table("a").join("b", ["key1", "key2"])
    assert "USING (`key1`, `key2`)" in df.generate_query()
