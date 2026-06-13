from __future__ import annotations

import pytest

from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_show(spark: SparkSession, capsys: pytest.CaptureFixture) -> None:
    spark.table("users").select("id").show()
    captured = capsys.readouterr()
    assert "SELECT" in captured.out
