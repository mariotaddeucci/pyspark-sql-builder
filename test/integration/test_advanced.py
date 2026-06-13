from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession

# ── Schema listing (cross-engine) ─────────────────────────────────────────


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


# ── Cast fields (cross-engine) ────────────────────────────────────────────


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


# ── Struct operations (DuckDB only) ───────────────────────────────────────


def test_read_struct_fields(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("events")
        .selectExpr("name", "metadata.age", "metadata.city")
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
        {"name": "Charlie", "age": 35, "city": "SF"},
    ]


def test_struct_column_in_select(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.table("events").select("name", "metadata").orderBy("name")
    data = result.toArrow().to_pylist()
    assert len(data) == 3
    assert data[0]["name"] == "Alice"
    assert data[0]["metadata"]["age"] == 30
    assert data[0]["metadata"]["city"] == "NYC"


# ── Array operations (DuckDB only) ────────────────────────────────────────


def test_array_length_and_contains(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("events")
        .selectExpr(
            "name",
            "array_length(tags) AS tag_count",
            "list_contains(tags, 'admin') AS is_admin",
        )
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "tag_count": 2, "is_admin": True},
        {"name": "Bob", "tag_count": 1, "is_admin": False},
        {"name": "Charlie", "tag_count": 3, "is_admin": True},
    ]


def test_array_to_string(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("events")
        .selectExpr("name", "array_to_string(tags, ', ') AS tags_str")
        .orderBy("name")
    )
    data = result.toArrow().to_pylist()
    assert data == [
        {"name": "Alice", "tags_str": "admin, user"},
        {"name": "Bob", "tags_str": "user"},
        {"name": "Charlie", "tags_str": "admin, editor, user"},
    ]


# ── Explode columns (DuckDB only) ─────────────────────────────────────────


def test_explode_array(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("events")
        .selectExpr("name", "UNNEST(tags) AS tag")
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


def test_explode_outer_with_nulls(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.sql("SELECT 'x' AS name, NULL AS tags").selectExpr(
        "name", "UNNEST(tags) AS tag"
    )
    data = result.toArrow().to_pylist()
    assert data == []


# ── Date conversions (DuckDB only) ────────────────────────────────────────


def test_date_part_extraction(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("transactions")
        .selectExpr(
            "id",
            "YEAR(CAST(date AS DATE)) AS year",
            "MONTH(CAST(date AS DATE)) AS month",
            "DAY(CAST(date AS DATE)) AS day",
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


def test_date_add_and_diff(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("transactions")
        .where(F.col("id") == 1)
        .selectExpr(
            "id",
            "CAST(date AS DATE) + 7 AS plus_7",
            "CAST(date AS DATE) - 1 AS minus_1",
            "DATEDIFF('day', CAST(date AS DATE),"
            " CAST('2024-01-10' AS DATE)) AS days_diff",
        )
    )
    data = result.toArrow().to_pylist()
    assert len(data) == 1
    row = data[0]
    assert row["id"] == 1
    assert row["days_diff"] == 9


def test_date_format(duckdb_spark: SparkSession) -> None:
    result = (
        duckdb_spark.table("transactions")
        .where(F.col("id") == 1)
        .selectExpr("strftime(CAST(date AS DATE), '%Y/%m/%d') AS formatted")
    )
    data = result.toArrow().to_pylist()
    assert data == [{"formatted": "2024/01/01"}]


# ── Series generation (DuckDB only) ───────────────────────────────────────


def test_range_basic(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.range(0, 5).select(F.col("id"))
    data = result.toArrow().to_pylist()
    assert data == [{"id": 0}, {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]


def test_range_with_step(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.range(0, 10, 3)
    data = result.toArrow().to_pylist()
    assert data == [{"id": 0}, {"id": 3}, {"id": 6}, {"id": 9}]


def test_range_empty(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.range(5, 5)
    data = result.toArrow().to_pylist()
    assert data == []
