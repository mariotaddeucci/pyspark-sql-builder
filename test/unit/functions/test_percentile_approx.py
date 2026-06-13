from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_percentile_approx() -> None:
    c = F.percentile_approx(F.col("x"), 0.5)
    assert c._expr == "PERCENTILE_APPROX(`x`, 0.5)"
