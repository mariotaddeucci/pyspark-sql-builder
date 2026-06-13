from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_find_in_set() -> None:
    c = F.find_in_set(F.col("val"), F.col("arr"))
    assert c._expr == "FIND_IN_SET(`val`, `arr`)"
