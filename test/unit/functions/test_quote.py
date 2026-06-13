from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_quote() -> None:
    c = F.quote(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
