from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_sort() -> None:
    c = F.array_sort(F.col("x"))
    assert c._expr == "ARRAY_SORT(`x`)"
