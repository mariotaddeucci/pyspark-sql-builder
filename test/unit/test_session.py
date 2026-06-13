from __future__ import annotations

from pyspark_sql_builder.readwriter import DataFrameReader
from pyspark_sql_builder.session import SparkSession


def test_builder_get_or_create() -> None:
    session = SparkSession.builder.app_name("test").getOrCreate()
    assert isinstance(session, SparkSession)
    assert session.dialect == "spark"


def test_table(spark: SparkSession) -> None:
    df = spark.table("users")
    assert df.generate_query() == "SELECT * FROM users"


def test_default_dialect() -> None:
    session = SparkSession()
    assert session.dialect == "spark"


def test_custom_dialect() -> None:
    session = SparkSession(dialect="duckdb")
    assert session.dialect == "duckdb"


def test_sql_method(spark: SparkSession) -> None:
    df = spark.sql("SELECT id, name FROM users")
    assert df.generate_query() == "SELECT id, name FROM users"


def test_read_property(spark: SparkSession) -> None:
    assert isinstance(spark.read, DataFrameReader)


def test_read_table(spark: SparkSession) -> None:
    df = spark.read.table("users")
    assert df.generate_query() == "SELECT * FROM users"


def test_range(spark: SparkSession) -> None:
    df = spark.range(0, 10)
    assert "range" in df.generate_query().lower()
