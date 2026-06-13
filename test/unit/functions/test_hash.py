from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_hash() -> None:
    c = F.hash(F.col("a"), F.col("b"))
    assert c._expr == "HASH(`a`, `b`)"
