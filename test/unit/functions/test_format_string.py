from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_format_string() -> None:
    c = F.format_string("Hello %s", F.col("x"))
    assert c._expr == "FORMAT_STRING('Hello %s', `x`)"
