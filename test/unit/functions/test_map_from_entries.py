from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_map_from_entries() -> None:
    c = F.map_from_entries(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
