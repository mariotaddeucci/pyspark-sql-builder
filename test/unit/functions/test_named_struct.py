from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_named_struct() -> None:
    c = F.named_struct("name", F.col("v"))
    assert c._expr == "NAMED_STRUCT('name', `v`)"
