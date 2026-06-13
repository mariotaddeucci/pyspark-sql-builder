from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regr_r2() -> None:
    c = F.regr_r2(F.col("x"), F.col("y"))
    assert c._expr == "REGR_R2(`x`, `y`)"
