from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_ifnull() -> None:
    c = F.ifnull(F.col("value"), 0)
    assert c._expr == "IFNULL(`value`, 0)"


def test_ifnull_with_string_col() -> None:
    c = F.ifnull("value", "default")
    assert c._expr == "IFNULL(`value`, 'default')"


def test_ifnull_with_null() -> None:
    c = F.ifnull(F.col("value"), None)
    assert c._expr == "IFNULL(`value`, NULL)"
