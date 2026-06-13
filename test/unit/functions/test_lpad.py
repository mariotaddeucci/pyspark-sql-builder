from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_lpad() -> None:
    c = F.lpad(F.col("x"), 10, "x")
    assert c._expr == "LPAD(`x`, 10, 'x')"
