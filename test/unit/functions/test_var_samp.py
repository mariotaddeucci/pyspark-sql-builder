from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_var_samp() -> None:
    c = F.var_samp(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
