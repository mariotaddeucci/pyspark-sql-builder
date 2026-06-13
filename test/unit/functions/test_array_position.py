from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_array_position() -> None:
    c = F.array_position(F.col("a"), 1)
    assert c._expr == "ARRAY_POSITION(`a`, 1)"
