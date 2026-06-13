from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_isnotnull() -> None:
    c = F.isnotnull(F.col("value"))
    assert c._expr == "`value` IS NOT NULL"
