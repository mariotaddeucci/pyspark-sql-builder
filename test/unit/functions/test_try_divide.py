from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_try_divide() -> None:
    c = F.try_divide(F.col("a"), F.col("b"))
    assert c._expr == "`a` / `b`"
