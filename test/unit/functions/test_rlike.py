from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_rlike() -> None:
    c = F.rlike(F.col("x"), "\\d+")
    assert c._expr == "`x` RLIKE '\\d+'"
