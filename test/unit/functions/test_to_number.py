from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_to_number() -> None:
    c = F.to_number(F.col("x"), "999")
    assert c._expr == "TO_NUMBER(`x`, '999')"
