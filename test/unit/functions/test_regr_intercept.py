from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regr_intercept() -> None:
    c = F.regr_intercept(F.col("x"), F.col("y"))
    assert c._expr == "REGR_INTERCEPT(`x`, `y`)"
