from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_map_from_arrays() -> None:
    c = F.map_from_arrays(F.col("k"), F.col("v"))
    assert c._expr == "MAP_FROM_ARRAYS(`k`, `v`)"
