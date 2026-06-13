from __future__ import annotations

import pytest

from pyspark_sql_builder.session import SparkSession


@pytest.fixture()
def spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


@pytest.fixture()
def duckdb() -> SparkSession:
    return SparkSession(dialect="duckdb")


@pytest.fixture()
def postgres() -> SparkSession:
    return SparkSession(dialect="postgres")


@pytest.fixture()
def bigquery() -> SparkSession:
    return SparkSession(dialect="bigquery")
