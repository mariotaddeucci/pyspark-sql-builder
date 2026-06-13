from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_power() -> None:
    c = F.power(F.col("x"), 2)
    assert c._expr == "POWER(`x`, 2)"
