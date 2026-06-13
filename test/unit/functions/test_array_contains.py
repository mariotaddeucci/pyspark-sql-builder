from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_contains() -> None:
    c = F.array_contains(F.col("a"), 1)
    assert c._expr == "ARRAY_CONTAINS(`a`, 1)"
