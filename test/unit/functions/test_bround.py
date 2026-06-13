from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_bround() -> None:
    c = F.bround(F.col("x"), 2)
    assert c._expr == "BROUND(`x`, 2)"
