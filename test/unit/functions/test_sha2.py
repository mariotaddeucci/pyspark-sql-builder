from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_sha2() -> None:
    c = F.sha2(F.col("x"), 256)
    assert c._expr == "SHA2(`x`, 256)"
