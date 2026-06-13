from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regexp_substr() -> None:
    c = F.regexp_substr(F.col("x"), "\\d+")
    assert c._expr == "REGEXP_SUBSTR(`x`, '\\d+')"
