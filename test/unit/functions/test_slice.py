from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_slice() -> None:
    c = F.slice(F.col("a"), 1, 3)
    assert c._expr == "SLICE(`a`, 1, 3)"
