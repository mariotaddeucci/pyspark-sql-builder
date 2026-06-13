from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_expm1() -> None:
    c = F.expm1(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
