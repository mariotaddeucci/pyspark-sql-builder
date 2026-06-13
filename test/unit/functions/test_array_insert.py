from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_insert() -> None:
    c = F.array_insert(F.col("a"), 1, 0)
    assert c._expr == "ARRAY_INSERT(`a`, 1, 0)"
