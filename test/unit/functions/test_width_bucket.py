from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_width_bucket() -> None:
    c = F.width_bucket(F.col("x"), 0, 100, 10)
    assert c._expr == "WIDTH_BUCKET(`x`, 0, 100, 10)"
