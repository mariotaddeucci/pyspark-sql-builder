from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_covar_samp() -> None:
    c = F.covar_samp(F.col("x"), F.col("y"))
    assert c._expr == "COVAR_SAMP(`x`, `y`)"
