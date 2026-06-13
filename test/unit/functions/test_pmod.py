from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_pmod() -> None:
    c = F.pmod(F.col("x"), 3)
    assert c._expr == "(`x` % 3)"
