"""Test automatic skip behavior with AnalysisException."""

from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_automatic_skip_with_missing_events_table(spark: SparkSession) -> None:
    """Test automatic skip when referenced tables are missing."""
    result = spark.table("events").select(F.col("name")).limit(1)
    data = result.toArrow().to_pylist()
    assert isinstance(data, list)


def test_automatic_skip_missing_table_in_join(spark: SparkSession) -> None:
    """Test automatic skip works for missing tables in complex queries."""
    result = spark.table("users").join("fake_table", "users.id = fake_table.user_id").select(F.col("users.name"))
    result.toArrow().to_pylist()
    assert False, "Test should have been skipped"
