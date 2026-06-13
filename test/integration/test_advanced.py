from __future__ import annotations

import pytest

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession

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


@pytest.mark.requires_tables("events")
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


@pytest.mark.requires_tables("events")
def test_struct_column_in_select(spark: SparkSession) -> None:
    result = spark.table("events").select("name", "metadata").orderBy("name")
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0]["name"] == "Alice"
    assert data[0]["metadata"]["age"] == 30
    assert data[0]["metadata"]["city"] == "NYC"


# ── Array operations (requires events table with TEXT[] type) ─────────


@pytest.mark.requires_tables("events")
def test_array_size_and_contains(spark: SparkSession) -> None:
    result = (
        spark.table("events")
        .select(
            F.col("name"),
            F.array_size(F.col("tags")).alias("tag_count"),
            F.array_contains(F.col("tags"), "admin").alias("is_admin"),
        )
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "tag_count": 2, "is_admin": True},
        {"name": "Bob", "tag_count": 1, "is_admin": False},
        {"name": "Charlie", "tag_count": 3, "is_admin": True},
    ]


@pytest.mark.requires_tables("events")
def test_array_join(spark: SparkSession) -> None:
    result = (
        spark.table("events")
        .select(
            F.col("name"),
            F.array_join(F.col("tags"), ", ").alias("tags_str"),
        )
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "tags_str": "admin, user"},
        {"name": "Bob", "tags_str": "user"},
        {"name": "Charlie", "tags_str": "admin, editor, user"},
    ]


# ── Explode columns (requires events table with TEXT[] type) ──────────


@pytest.mark.requires_tables("events")
def test_explode_array(spark: SparkSession) -> None:
    result = (
        spark.table("events")
        .select(F.col("name"), F.explode(F.col("tags")).alias("tag"))
        .orderBy("name", "tag")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "tag": "admin"},
        {"name": "Alice", "tag": "user"},
        {"name": "Bob", "tag": "user"},
        {"name": "Charlie", "tag": "admin"},
        {"name": "Charlie", "tag": "editor"},
        {"name": "Charlie", "tag": "user"},
    ]


# ── Date conversions ─────────────────────────────────────────────────


def test_date_part_extraction(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .select(
            F.col("id"),
            F.year(F.col("date")).alias("year"),
            F.month(F.col("date")).alias("month"),
            F.day(F.col("date")).alias("day"),
        )
        .orderBy("id")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"id": 1, "year": 2024, "month": 1, "day": 1},
        {"id": 2, "year": 2024, "month": 1, "day": 15},
        {"id": 3, "year": 2024, "month": 2, "day": 1},
        {"id": 4, "year": 2024, "month": 2, "day": 15},
        {"id": 5, "year": 2024, "month": 3, "day": 1},
        {"id": 6, "year": 2024, "month": 1, "day": 10},
        {"id": 7, "year": 2024, "month": 2, "day": 20},
    ]


def test_date_add_and_diff(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .where(F.col("id") == 1)
        .select(
            F.col("id"),
            F.date_add(F.col("date"), 7).alias("plus_7"),
            F.date_sub(F.col("date"), 1).alias("minus_1"),
            F.datediff(F.lit("2024-01-10"), F.col("date")).alias("days_diff"),
        )
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 1
    row = data[0]
    assert row["id"] == 1
    assert row["days_diff"] == 9


def test_date_format(spark: SparkSession) -> None:
    result = (
        spark.table("transactions")
        .where(F.col("id") == 1)
        .select(F.date_format(F.col("date"), "yyyy/MM/dd").alias("formatted"))
    )
    data = result.toArrow().to_pylist()
    assert data == [{"formatted": "2024/01/01"}]


# ── Series generation ────────────────────────────────────────────────


def test_range_basic(spark: SparkSession) -> None:
    result = spark.range(0, 5).select(F.col("id"))
    data = result.toArrow().to_pylist()
    assert data == [{"id": 0}, {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]


def test_range_with_step(spark: SparkSession) -> None:
    result = spark.range(0, 10, 3)
    data = result.toArrow().to_pylist()
    assert data == [{"id": 0}, {"id": 3}, {"id": 6}, {"id": 9}]


def test_range_empty(spark: SparkSession) -> None:
    result = spark.range(5, 5)
    data = result.toArrow().to_pylist()
    assert data == []
