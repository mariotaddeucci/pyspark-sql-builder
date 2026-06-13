from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_lag() -> None:
    c = F.lag(F.col("x"))
    assert c._expr == "LAG(`x`, 1, NULL)"
