from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_repeat() -> None:
    c = F.repeat(F.col("x"), 3)
    assert c._expr == "REPEAT(`x`, 3)"
