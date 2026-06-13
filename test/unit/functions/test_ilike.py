from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_ilike() -> None:
    c = F.ilike(F.col("name"), "%john%")
    assert c._expr == "`name` ILIKE '%john%'"
