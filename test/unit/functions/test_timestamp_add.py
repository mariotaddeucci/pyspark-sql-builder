from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_timestamp_add() -> None:
    c = F.timestamp_add(F.col("ts"), 3)
    assert c._expr == "`ts` + INTERVAL 3 DAYS"
