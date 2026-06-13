from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_contains() -> None:
    c = F.contains(F.col("x"), "sub")
    assert c._expr == "CONTAINS(`x`, 'sub')"
