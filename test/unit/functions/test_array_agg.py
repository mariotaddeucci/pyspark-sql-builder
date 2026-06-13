from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_agg() -> None:
    c = F.array_agg(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
