from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import Window
from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_basic_join_agg(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .join("users", F.col("transactions.user_id") == F.col("users.id"))
        .select(
            F.col("users.name").alias("user_name"),
            F.col("transactions.amount"),
            F.col("transactions.date"),
        )
        .groupBy(F.col("user_name"), F.col("date"))
        .agg(F.sum(F.col("amount")).alias("balance"))
        .orderBy(F.col("user_name"), F.col("date"))
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 7
    assert data[0] == {"user_name": "Joao", "date": "2024-01-01", "balance": 100.0}
    assert data[1] == {"user_name": "Joao", "date": "2024-01-15", "balance": -50.0}
    assert data[2] == {"user_name": "Joao", "date": "2024-02-20", "balance": 25.0}
    assert data[3] == {"user_name": "Maria", "date": "2024-02-01", "balance": 200.0}
    assert data[4] == {"user_name": "Maria", "date": "2024-02-15", "balance": -30.0}
    assert data[5] == {"user_name": "Maria", "date": "2024-03-01", "balance": 80.0}
    assert data[6] == {"user_name": "Pedro", "date": "2024-01-10", "balance": 500.0}


def test_window_function(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .select(
            F.col("user_id"),
            F.col("amount"),
            F.row_number().over(Window.partitionBy("user_id").orderBy(F.col("amount").desc())).alias("rn"),
        )
        .orderBy(F.col("user_id"), F.col("rn"))
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 7
    assert data[0] == {"user_id": 1, "amount": 100.0, "rn": 1}
    assert data[1] == {"user_id": 1, "amount": 25.0, "rn": 2}
    assert data[2] == {"user_id": 1, "amount": -50.0, "rn": 3}
    assert data[3] == {"user_id": 2, "amount": 200.0, "rn": 1}
    assert data[4] == {"user_id": 2, "amount": 80.0, "rn": 2}
    assert data[5] == {"user_id": 2, "amount": -30.0, "rn": 3}
    assert data[6] == {"user_id": 3, "amount": 500.0, "rn": 1}


def test_join_using(spark: SparkSession) -> None:
    result = (
        spark.table("users")
        .join("regions", ["region_id"])
        .select(
            F.col("users.name"),
            F.col("users.email"),
            F.col("regions.name").alias("region"),
        )
        .orderBy(F.col("name"))
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0] == {"name": "Joao", "email": "joao@email.com", "region": "North"}
    assert data[1] == {"name": "Maria", "email": "maria@email.com", "region": "South"}
    assert data[2] == {"name": "Pedro", "email": "pedro@email.com", "region": "North"}


def test_filter_and_groupby(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .where(F.col("amount") > 0)
        .where(F.col("date") >= "2024-02-01")
        .groupBy(F.col("date"))
        .agg(F.sum(F.col("amount")).alias("total"))
        .orderBy(F.col("date"))
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0] == {"date": "2024-02-01", "total": 200.0}
    assert data[1] == {"date": "2024-02-20", "total": 25.0}
    assert data[2] == {"date": "2024-03-01", "total": 80.0}


def test_multiple_joins_and_agg(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .join("users", F.col("transactions.user_id") == F.col("users.id"))
        .join("categories", F.col("transactions.category_id") == F.col("categories.id"))
        .select(
            F.col("users.name").alias("user_name"),
            F.col("categories.name").alias("category_name"),
            F.col("amount"),
        )
        .where(F.col("amount") > 0)
        .groupBy(F.col("user_name"), F.col("category_name"))
        .agg(
            F.sum(F.col("amount")).alias("total"),
            F.count(F.col("amount")).alias("count"),
        )
        .orderBy(F.col("user_name"), F.col("category_name"))
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0] == {
        "user_name": "Joao",
        "category_name": "food",
        "total": 125.0,
        "count": 2,
    }
    assert data[1] == {
        "user_name": "Maria",
        "category_name": "entertainment",
        "total": 280.0,
        "count": 2,
    }
    assert data[2] == {
        "user_name": "Pedro",
        "category_name": "food",
        "total": 500.0,
        "count": 1,
    }
