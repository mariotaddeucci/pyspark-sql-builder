from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regexp_like() -> None:
    c = F.regexp_like(F.col("x"), "\\d+")
    assert c._expr == "`x` RLIKE '\\d+'"
