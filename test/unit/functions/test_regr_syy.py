from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regr_syy() -> None:
    c = F.regr_syy(F.col("x"), F.col("y"))
    assert c._expr == "REGR_SYY(`x`, `y`)"
