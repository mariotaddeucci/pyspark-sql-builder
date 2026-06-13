from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_approx_percentile() -> None:
    c = F.approx_percentile(F.col("x"), 0.5)
    assert c._expr == "APPROX_PERCENTILE(`x`, 0.5)"
