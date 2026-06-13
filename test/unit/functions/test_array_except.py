from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_except() -> None:
    c = F.array_except(F.col("a"), F.col("b"))
    assert c._expr == "ARRAY_EXCEPT(`a`, `b`)"
