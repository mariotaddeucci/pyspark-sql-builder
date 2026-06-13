from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_json_object_keys() -> None:
    c = F.json_object_keys(F.col("j"))
    assert c._expr == "JSON_OBJECT_KEYS(`j`)"
