from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_decode() -> None:
    c = F.decode(F.col("x"), "UTF-8")
    assert c._expr == "DECODE(`x`, 'UTF-8')"
