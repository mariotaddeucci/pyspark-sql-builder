from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_base64() -> None:
    c = F.base64(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
