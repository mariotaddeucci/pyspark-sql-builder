from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regr_sxx() -> None:
    c = F.regr_sxx(F.col("x"), F.col("y"))
    assert c._expr == "REGR_SXX(`x`, `y`)"
