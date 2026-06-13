from __future__ import annotations

from pyspark_sql_builder.session import SparkSession


def test_builder_get_or_create() -> None:
    session = SparkSession.builder.app_name("test").getOrCreate()
    assert isinstance(session, SparkSession)
    assert session.dialect == "spark"
