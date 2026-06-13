from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_conv() -> None:
    c = F.conv(F.col("x"), 10, 16)
    assert c._expr == "CONV(`x`, 10, 16)"
