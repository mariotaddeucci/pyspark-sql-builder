from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_append() -> None:
    c = F.array_append(F.col("a"), 1)
    assert c._expr == "ARRAY_APPEND(`a`, 1)"
