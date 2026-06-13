from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_rpad() -> None:
    c = F.rpad(F.col("x"), 10, "x")
    assert c._expr == "RPAD(`x`, 10, 'x')"
