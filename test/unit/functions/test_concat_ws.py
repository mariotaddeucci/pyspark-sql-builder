from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_concat_ws() -> None:
    c = F.concat_ws(",", F.col("a"), F.col("b"))
    assert c._expr == "CONCAT_WS(',', `a`, `b`)"
