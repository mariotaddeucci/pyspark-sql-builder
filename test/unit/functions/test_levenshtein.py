from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_levenshtein() -> None:
    c = F.levenshtein(F.col("a"), F.col("b"))
    assert c._expr == "LEVENSHTEIN(`a`, `b`)"
