from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_btrim() -> None:
    c = F.btrim(F.col("x"))
    assert c._expr == "BTRIM(`x`)"
