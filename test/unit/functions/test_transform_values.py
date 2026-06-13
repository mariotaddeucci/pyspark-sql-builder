from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_transform_values() -> None:
    c = F.transform_values(F.col("m"), "(k, v) -> v")
    assert c._expr == "TRANSFORM_VALUES(`m`, (k, v) -> v)"
