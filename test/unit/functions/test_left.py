from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_left() -> None:
    c = F.left(F.col("x"), 3)
    assert c._expr == "LEFT(`x`, 3)"
