from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_remove() -> None:
    c = F.array_remove(F.col("a"), 1)
    assert c._expr == "ARRAY_REMOVE(`a`, 1)"
