from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_format_number() -> None:
    c = F.format_number(F.col("x"), 2)
    assert c._expr == "FORMAT_NUMBER(`x`, 2)"
