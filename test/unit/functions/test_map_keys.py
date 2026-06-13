from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_map_keys() -> None:
    c = F.map_keys(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
