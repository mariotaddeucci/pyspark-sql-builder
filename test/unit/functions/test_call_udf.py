from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_call_udf() -> None:
    c = F.call_udf("my_udf", F.col("x"))
    assert c._expr == "my_udf(`x`)"
