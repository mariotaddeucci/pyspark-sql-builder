from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_is_valid_utf8() -> None:
    c = F.is_valid_utf8(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
