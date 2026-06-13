from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_string_agg() -> None:
    c = F.string_agg(F.col("x"), ",")
    assert c._expr == "STRING_AGG(`x`, ',')"
