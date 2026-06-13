from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_repeat() -> None:
    c = F.array_repeat(F.col("x"), 3)
    assert c._expr == "ARRAY_REPEAT(`x`, 3)"
