from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_json_array_length() -> None:
    c = F.json_array_length(F.col("j"))
    assert c._expr == "JSON_ARRAY_LENGTH(`j`)"
