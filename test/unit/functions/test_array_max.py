from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_max() -> None:
    c = F.array_max(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
