from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regr_sxy() -> None:
    c = F.regr_sxy(F.col("x"), F.col("y"))
    assert c._expr == "REGR_SXY(`x`, `y`)"
