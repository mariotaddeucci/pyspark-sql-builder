from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regexp_extract_all() -> None:
    c = F.regexp_extract_all(F.col("x"), "(\\d+)", 1)
    assert c._expr == "REGEXP_EXTRACT_ALL(`x`, '(\\d+)', 1)"
