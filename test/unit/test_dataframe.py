from __future__ import annotations

import pytest

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


def test_select_all(spark: SparkSession) -> None:
    df = spark.table("users")
    assert df.generate_query() == "SELECT * FROM users"


def test_select_columns(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    assert df.generate_query() == "SELECT `id`, `name` FROM users"


def test_select_column_objects(spark: SparkSession) -> None:
    df = spark.table("users").select(F.col("id"), F.col("name"))
    assert df.generate_query() == "SELECT `id`, `name` FROM users"


def test_where_condition(spark: SparkSession) -> None:
    df = spark.table("users").where(F.col("age") > 18)
    assert df.generate_query() == "SELECT * FROM users WHERE `age` > 18"


def test_multiple_where(spark: SparkSession) -> None:
    df = (
        spark.table("users").where(F.col("age") > 18).where(F.col("status") == "active")
    )
    expected = "SELECT * FROM users WHERE `age` > 18 AND `status` = 'active'"
    assert df.generate_query() == expected


def test_select_with_where(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name", "age").where(F.col("age") >= 21)
    expected = "SELECT `id`, `name`, `age` FROM users WHERE `age` >= 21"
    assert df.generate_query() == expected


def test_filter(spark: SparkSession) -> None:
    df = spark.table("users").filter(F.col("active") == True)  # noqa: E712
    assert df.generate_query() == "SELECT * FROM users WHERE `active` = TRUE"


def test_order_by(spark: SparkSession) -> None:
    df = spark.table("users").orderBy(F.col("name").asc())
    assert df.generate_query() == "SELECT * FROM users ORDER BY `name` ASC"


def test_order_by_multiple(spark: SparkSession) -> None:
    df = spark.table("users").orderBy(F.col("age").desc(), F.col("name").asc())
    assert df.generate_query() == "SELECT * FROM users ORDER BY `age` DESC, `name` ASC"


def test_limit(spark: SparkSession) -> None:
    df = spark.table("users").limit(10)
    assert df.generate_query() == "SELECT * FROM users LIMIT 10"


def test_limit_with_offset(spark: SparkSession) -> None:
    df = spark.table("users").limit(10).offset(20)
    assert df.generate_query() == "SELECT * FROM users LIMIT 10 OFFSET 20"


def test_distinct(spark: SparkSession) -> None:
    df = spark.table("users").select("city").distinct()
    assert df.generate_query() == "SELECT DISTINCT `city` FROM users"


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


def test_alias(spark: SparkSession) -> None:
    df = spark.table("users").alias("u")
    assert df.generate_query() == "SELECT * FROM users AS u"


def test_union_all(spark: SparkSession) -> None:
    df1 = spark.table("users_2023")
    df2 = spark.table("users_2024")
    result = df1.unionAll(df2)
    assert "UNION ALL" in result.generate_query()


def test_aggregate(spark: SparkSession) -> None:
    df = spark.table("sales").agg(
        F.count(F.col("id")).alias("num_orders"),
        F.sum(F.col("amount")).alias("total_amount"),
    )
    result = df.generate_query()
    assert "COUNT(`id`)" in result
    assert "SUM(`amount`)" in result


def test_with_column(spark: SparkSession) -> None:
    df = (
        spark.table("users")
        .select("id", "price")
        .withColumn("total", F.col("price") * F.lit(1.1))
    )
    result = df.generate_query()
    assert "total" in result


def test_with_column_renamed(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    df = df.withColumnRenamed("name", "username")
    result = df.generate_query()
    assert "username" in result


def test_drop(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name", "age").drop("age")
    result = df.generate_query()
    assert "id" in result
    assert "name" in result
    assert "age" not in result


def test_full_pipeline(spark: SparkSession) -> None:
    df = (
        spark.table("orders")
        .join("customers", F.col("orders.customer_id") == F.col("customers.id"))
        .select("orders.id", "customers.name", "orders.amount")
        .where(F.col("orders.amount") > 100)
        .orderBy(F.col("orders.amount").desc())
        .limit(50)
    )
    result = df.generate_query()
    assert "SELECT" in result
    assert "FROM orders" in result
    assert "JOIN customers" in result
    assert "WHERE" in result
    assert "ORDER BY" in result
    assert "LIMIT 50" in result


def test_copy(spark: SparkSession) -> None:
    df1 = spark.table("users").select("id", "name")
    df2 = df1.copy()
    assert df1.generate_query() == df2.generate_query()


@pytest.mark.parametrize("dialect", ["spark", "duckdb", "postgres", "bigquery"])
def test_transpile_simple(dialect: str) -> None:
    session = SparkSession(dialect=dialect)
    df = session.table("users").select("id", "name").where(F.col("age") > 18)
    result = df.generate_query()
    assert "SELECT" in result or "select" in result
    assert result


def test_show(spark: SparkSession, capsys: pytest.CaptureFixture) -> None:
    spark.table("users").select("id").show()
    captured = capsys.readouterr()
    assert "SELECT" in captured.out


def test_group_by_agg(spark: SparkSession) -> None:
    df = spark.table("sales").select(
        F.col("category"), F.sum(F.col("amount")).alias("total")
    )
    grouped = df.groupBy("category")
    assert grouped is not None


def test_group_by_having_agg(spark: SparkSession) -> None:
    df = (
        spark.table("sales")
        .select(F.col("category"), F.sum(F.col("amount")).alias("total"))
        .having(F.sum(F.col("amount")) > 1000)
    )
    result = df.generate_query()
    assert "HAVING" in result
