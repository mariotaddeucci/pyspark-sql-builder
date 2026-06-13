from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_overlay() -> None:
    c = F.overlay(F.col("x"), "rep", 3)
    assert c._expr == "OVERLAY(`x` PLACING 'rep' FROM 3)"
