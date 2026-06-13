from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_like() -> None:
    c = F.like(F.col("name"), "%foo%")
    assert c._expr == "`name` LIKE '%foo%'"
