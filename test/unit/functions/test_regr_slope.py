from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regr_slope() -> None:
    c = F.regr_slope(F.col("x"), F.col("y"))
    assert c._expr == "REGR_SLOPE(`x`, `y`)"
