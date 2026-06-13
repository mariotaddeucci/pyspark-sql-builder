from __future__ import annotations

import pytest

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


@pytest.mark.parametrize("dialect", ["spark", "duckdb", "postgres", "bigquery"])
def test_transpile_simple(dialect: str) -> None:
    session = SparkSession(dialect=dialect)
    df = session.table("users").select("id", "name").where(F.col("age") > 18)
    result = df.generate_query()
    assert "SELECT" in result or "select" in result
    assert result
