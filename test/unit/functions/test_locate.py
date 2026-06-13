from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_locate() -> None:
    c = F.locate("sub", F.col("x"))
    assert c._expr == "LOCATE('sub', `x`)"
