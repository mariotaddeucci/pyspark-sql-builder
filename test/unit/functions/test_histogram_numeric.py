from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_histogram_numeric() -> None:
    c = F.histogram_numeric(F.col("x"), 10)
    assert c._expr == "HISTOGRAM_NUMERIC(`x`, 10)"
