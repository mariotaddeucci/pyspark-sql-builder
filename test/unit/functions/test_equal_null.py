from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_equal_null() -> None:
    c = F.equal_null(F.col("a"), F.col("b"))
    assert c._expr == "`a` <=> `b`"


def test_equal_null_with_null() -> None:
    c = F.equal_null(F.col("a"), None)
    assert c._expr == "`a` <=> NULL"
