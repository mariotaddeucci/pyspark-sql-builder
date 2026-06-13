from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_array_join() -> None:
    c = F.array_join(F.col("a"), ",")
    assert c._expr == "ARRAY_JOIN(`a`, ',')"
