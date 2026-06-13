from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_explode_outer() -> None:
    c = F.explode_outer(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
