from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_map_filter() -> None:
    c = F.map_filter(F.col("m"), "(k, v) -> v")
    assert c._expr == "MAP_FILTER(`m`, (k, v) -> v)"
