from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_arrays_overlap() -> None:
    c = F.arrays_overlap(F.col("a"), F.col("b"))
    assert c._expr == "ARRAYS_OVERLAP(`a`, `b`)"
