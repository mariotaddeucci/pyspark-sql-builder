from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_zip_with() -> None:
    c = F.zip_with(F.col("a"), F.col("b"), "(x, y) -> x + y")
    assert c._expr == "ZIP_WITH(`a`, `b`, (x, y) -> x + y)"
