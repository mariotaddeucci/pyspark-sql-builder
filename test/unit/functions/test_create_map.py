from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_create_map() -> None:
    c = F.create_map(F.col("k"), F.col("v"))
    assert c._expr == "MAP(`k`, `v`)"
