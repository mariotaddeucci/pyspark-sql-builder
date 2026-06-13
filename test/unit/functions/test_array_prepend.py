from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_prepend() -> None:
    c = F.array_prepend(F.col("a"), 0)
    assert c._expr == "ARRAY_PREPEND(`a`, 0)"
