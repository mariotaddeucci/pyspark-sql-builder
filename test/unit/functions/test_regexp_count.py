from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regexp_count() -> None:
    c = F.regexp_count(F.col("x"), "\\d+")
    assert c._expr == "REGEXP_COUNT(`x`, '\\d+')"
