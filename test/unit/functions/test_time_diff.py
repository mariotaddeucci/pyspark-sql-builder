from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_time_diff() -> None:
    c = F.time_diff("HOUR", F.col("start"), F.col("end"))
    assert c._expr == "TIME_DIFF(HOUR, `start`, `end`)"
