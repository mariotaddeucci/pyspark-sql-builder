from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_replace() -> None:
    c = F.replace(F.col("x"), "a", "b")
    assert c._expr == "REPLACE(`x`, 'a', 'b')"
