from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_shiftrightunsigned() -> None:
    c = F.shiftrightunsigned(F.col("x"), 1)
    assert c._expr == "`x` >> 1"
