from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_printf() -> None:
    c = F.printf("Hello %s", F.col("x"))
    assert c._expr == "PRINTF('Hello %s', `x`)"
