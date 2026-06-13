from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_startswith() -> None:
    c = F.startswith(F.col("x"), "pre")
    assert c._expr == "`x` LIKE 'pre' || '%'"
