from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_map_concat() -> None:
    c = F.map_concat(F.col("m1"), F.col("m2"))
    assert c._expr == "MAP_CONCAT(`m1`, `m2`)"
