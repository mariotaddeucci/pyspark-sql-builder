from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_forall() -> None:
    c = F.forall(F.col("a"), "x -> x > 0")
    assert c._expr == "FORALL(`a`, x -> x > 0)"
