from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_to_char() -> None:
    c = F.to_char(F.col("x"), "999")
    assert c._expr == "TO_CHAR(`x`, '999')"
