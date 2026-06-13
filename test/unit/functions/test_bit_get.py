from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_bit_get() -> None:
    c = F.bit_get(F.col("x"), 0)
    assert c._expr == "BIT_GET(`x`, 0)"
