from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_shiftright() -> None:
    c = F.shiftright(F.col("x"), 1)
    assert c._expr == "`x` >> 1"
