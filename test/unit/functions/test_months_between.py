from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_months_between() -> None:
    c = F.months_between(F.col("d1"), F.col("d2"))
    assert c._expr == "MONTHS_BETWEEN(`d1`, `d2`)"
