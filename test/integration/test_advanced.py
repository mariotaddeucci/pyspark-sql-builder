from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession

# ── Schema listing ───────────────────────────────────────────────────


def test_schema_after_select(spark: SparkSession) -> None:
    df = spark.table("users").select(
        F.col("id"),
        F.col("name").alias("username"),
        F.col("email"),
    )
    assert df.columns == ["id", "username", "email"]


def test_dtypes_after_cast(spark: SparkSession) -> None:
    df = spark.table("users").select(
        F.col("id").cast("DOUBLE").alias("id_dbl"),
        F.col("name"),
    )
    dtypes = dict(df.dtypes)
    assert dtypes["id_dbl"] == "double"
    assert dtypes["name"] == "string"


# ── Cast fields ──────────────────────────────────────────────────────


def test_cast_numeric_types(spark: SparkSession) -> None:
    result = (
        spark.table("users")
        .select(
            F.col("id"),
            F.col("id").cast("DOUBLE").alias("id_float"),
            F.col("name").cast("VARCHAR").alias("name_str"),
        )
        .orderBy("id")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"id": 1, "id_float": 1.0, "name_str": "Joao"},
        {"id": 2, "id_float": 2.0, "name_str": "Maria"},
        {"id": 3, "id_float": 3.0, "name_str": "Pedro"},
    ]


def test_cast_to_integer(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .select(
            F.col("id"),
            F.col("amount").cast("INTEGER").alias("amount_int"),
        )
        .orderBy("id")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"id": 1, "amount_int": 100},
        {"id": 2, "amount_int": -50},
        {"id": 3, "amount_int": 200},
        {"id": 4, "amount_int": -30},
        {"id": 5, "amount_int": 80},
        {"id": 6, "amount_int": 500},
        {"id": 7, "amount_int": 25},
    ]


# ── Struct operations (requires events table with STRUCT type) ────────


def test_read_struct_fields(spark: SparkSession) -> None:
    result = (
        spark.table("events")
        .selectExpr("name", "metadata.age", "metadata.city")
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
        {"name": "Charlie", "age": 35, "city": "SF"},
    ]


def test_struct_column_in_select(spark: SparkSession) -> None:
    result = spark.table("events").select("name", "metadata").orderBy("name")
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0]["name"] == "Alice"
    assert data[0]["metadata"]["age"] == 30
    assert data[0]["metadata"]["city"] == "NYC"


# ── Array operations (requires events table with TEXT[] type) ─────────


# ── Series generation ────────────────────────────────────────────────
