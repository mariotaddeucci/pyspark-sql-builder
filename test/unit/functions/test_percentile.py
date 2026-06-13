from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_percentile() -> None:
    c = F.percentile(F.col("x"), 0.5)
    assert c._expr == "PERCENTILE(`x`, 0.5)"
