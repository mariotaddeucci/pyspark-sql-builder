from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_time_trunc() -> None:
    c = F.time_trunc("HOUR", F.col("t"))
    assert c._expr == "TIME_TRUNC('HOUR', `t`)"
