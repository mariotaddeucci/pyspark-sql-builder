from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_st_setsrid() -> None:
    c = F.st_setsrid(F.col("x"), 4326)
    assert c._expr == "ST_SETSRID(`x`, 4326)"
