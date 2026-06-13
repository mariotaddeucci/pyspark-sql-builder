from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_map_zip_with() -> None:
    c = F.map_zip_with(F.col("m1"), F.col("m2"), "(k, v1, v2) -> v1")
    assert c._expr == "MAP_ZIP_WITH(`m1`, `m2`, (k, v1, v2) -> v1)"
