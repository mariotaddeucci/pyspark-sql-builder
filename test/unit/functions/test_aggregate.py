from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_aggregate() -> None:
    c = F.aggregate(F.col("arr"), F.lit(0), "(acc, x) -> acc + x")
    assert c._expr == "AGGREGATE(`arr`, 0, (acc, x) -> acc + x)"
