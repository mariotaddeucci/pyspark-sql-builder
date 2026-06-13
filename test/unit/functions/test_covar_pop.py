from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_covar_pop() -> None:
    c = F.covar_pop(F.col("x"), F.col("y"))
    assert c._expr == "COVAR_POP(`x`, `y`)"
