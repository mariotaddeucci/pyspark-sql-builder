from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_greatest() -> None:
    c = F.greatest(F.col("a"), F.col("b"))
    assert c._expr == "GREATEST(`a`, `b`)"
