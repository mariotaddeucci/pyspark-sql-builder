from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_collate() -> None:
    c = F.collate(F.col("x"), "UTF8")
    assert c._expr == "`x` COLLATE UTF8"
