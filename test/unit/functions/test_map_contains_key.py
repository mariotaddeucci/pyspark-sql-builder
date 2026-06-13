from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_map_contains_key() -> None:
    c = F.map_contains_key(F.col("m"), "k")
    assert c._expr == "MAP_CONTAINS_KEY(`m`, 'k')"
