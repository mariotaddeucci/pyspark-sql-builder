from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_min_by() -> None:
    c = F.min_by(F.col("x"), F.col("y"))
    assert c._expr == "MIN_BY(`x`, `y`)"
