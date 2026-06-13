from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regexp_extract() -> None:
    c = F.regexp_extract(F.col("x"), "(\\d+)", 1)
    assert c._expr == "REGEXP_EXTRACT(`x`, '(\\d+)', 1)"
