from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_try_multiply() -> None:
    c = F.try_multiply(F.col("a"), F.col("b"))
    assert c._expr == "`a` * `b`"
