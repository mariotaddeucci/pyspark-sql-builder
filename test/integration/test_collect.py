"""Integration tests for DataFrame.collect() method."""

from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.session import SparkSession
from pyspark_sql_builder.pyspark.sql.types import Row


def test_collect_multiple_rows(spark: SparkSession) -> None:
    """Test collect() with multiple rows from actual table."""
    df = spark.table("transactions").limit(3)
    rows = df.collect()
    assert len(rows) == 3
    assert all(isinstance(row, Row) for row in rows)
    assert "user_id" in rows[0].asDict()
    assert "amount" in rows[0].asDict()


def test_collect_row_access_by_name(spark: SparkSession) -> None:
    """Test accessing Row values by column name."""
    df = spark.table("transactions").limit(1)
    rows = df.collect()
    row = rows[0]
    assert row["user_id"] is not None
    assert row["amount"] is not None


def test_collect_row_access_by_attribute(spark: SparkSession) -> None:
    """Test accessing Row values by attribute name."""
    df = spark.table("transactions").limit(1)
    rows = df.collect()
    row = rows[0]
    assert row.user_id is not None
    assert row.amount is not None


def test_collect_empty_dataframe(spark: SparkSession) -> None:
    """Test collect() on empty DataFrame."""
    df = spark.sql("SELECT 1 AS id, 'Alice' AS name LIMIT 0")
    rows = df.collect()
    assert len(rows) == 0
    assert isinstance(rows, list)


def test_collect_with_null_values(spark: SparkSession) -> None:
    """Test collect() with NULL values."""
    # Use a table-based approach to avoid NULL type inference issues
    query = (
        "SELECT 1 AS id, 'Alice' AS name UNION ALL "
        "SELECT 2, 'Bob' UNION ALL SELECT 3, NULL"
    )
    df = spark.sql(query)
    rows = df.collect()
    assert len(rows) == 3
    assert rows[0]["id"] == 1
    assert rows[0]["name"] == "Alice"
    assert rows[1]["id"] == 2
    assert rows[1]["name"] == "Bob"
    assert rows[2]["id"] == 3
    assert rows[2]["name"] is None


def test_collect_row_as_dict(spark: SparkSession) -> None:
    """Test converting collected Row to dictionary."""
    df = spark.sql("SELECT 1 AS id, 'Alice' AS name, 30 AS age")
    rows = df.collect()
    row_dict = rows[0].asDict()
    assert row_dict == {"age": 30, "id": 1, "name": "Alice"}


def test_collect_row_iteration(spark: SparkSession) -> None:
    """Test iterating over Row values."""
    df = spark.sql("SELECT 1 AS id, 'Alice' AS name")
    rows = df.collect()
    values = list(rows[0])
    # Values are sorted by column name
    assert values == [1, "Alice"]


def test_collect_row_len(spark: SparkSession) -> None:
    """Test Row length from collected data."""
    df = spark.sql("SELECT 1 AS id, 'Alice' AS name, 30 AS age")
    rows = df.collect()
    assert len(rows[0]) == 3


def test_collect_with_select_and_filter(spark: SparkSession) -> None:
    """Test collect() after select and filter operations."""
    df = spark.sql("SELECT 1 AS id, 'Alice' AS name, 30 AS age").selectExpr(
        "id", "name"
    )
    rows = df.collect()
    assert len(rows) == 1
    assert len(rows[0]) == 2  # Only id and name columns
    assert rows[0]["id"] == 1
    assert rows[0]["name"] == "Alice"


def test_collect_after_groupby(spark: SparkSession) -> None:
    """Test collect() after groupBy aggregation."""
    from pyspark_sql_builder.pyspark.sql import functions as F

    df = (
        spark.table("transactions")
        .groupBy(F.col("user_id"))
        .agg(F.sum(F.col("amount")).alias("total_amount"))
        .limit(3)
    )
    rows = df.collect()
    assert len(rows) == 3
    assert all(isinstance(row, Row) for row in rows)
    for row in rows:
        assert row["user_id"] is not None
        assert row["total_amount"] is not None
