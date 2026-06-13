from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_default_dialect() -> None:
    session = SparkSession()
    assert session.dialect == "spark"


def test_custom_dialect() -> None:
    session = SparkSession(dialect="duckdb")
    assert session.dialect == "duckdb"
