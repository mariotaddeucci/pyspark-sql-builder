from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_nth_value() -> None:
    c = F.nth_value(F.col("x"), 2)
    assert c._expr == "NTH_VALUE(`x`, 2)"
