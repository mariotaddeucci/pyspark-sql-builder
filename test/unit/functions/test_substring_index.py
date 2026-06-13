from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_substring_index() -> None:
    c = F.substring_index(F.col("x"), ".", 2)
    assert c._expr == "SUBSTRING_INDEX(`x`, '.', 2)"
