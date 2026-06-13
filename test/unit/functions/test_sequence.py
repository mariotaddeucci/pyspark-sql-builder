from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_sequence() -> None:
    c = F.sequence(F.lit(1), F.lit(10))
    assert c._expr == "SEQUENCE(1, 10)"
