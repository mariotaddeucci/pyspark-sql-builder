from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_encode() -> None:
    c = F.encode(F.col("x"), "UTF-8")
    assert c._expr == "ENCODE(`x`, 'UTF-8')"
