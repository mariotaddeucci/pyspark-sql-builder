from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_lead() -> None:
    c = F.lead(F.col("x"))
    assert c._expr == "LEAD(`x`, 1, NULL)"
