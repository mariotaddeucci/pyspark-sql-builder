from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_reduce() -> None:
    c = F.reduce(F.col("a"), F.lit(0), "(acc, x) -> acc + x")
    assert c._expr == "REDUCE(`a`, 0, (acc, x) -> acc + x)"
