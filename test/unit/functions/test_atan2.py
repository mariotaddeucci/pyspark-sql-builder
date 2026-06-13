from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_atan2() -> None:
    c = F.atan2(F.col("y"), F.col("x"))
    assert c._expr == "ATAN2(`y`, `x`)"
