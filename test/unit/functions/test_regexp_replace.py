from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regexp_replace() -> None:
    c = F.regexp_replace(F.col("x"), "\\d+", "n")
    assert c._expr == "REGEXP_REPLACE(`x`, '\\d+', 'n', 1)"
