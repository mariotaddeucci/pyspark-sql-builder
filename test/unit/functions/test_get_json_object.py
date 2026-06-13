from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_get_json_object() -> None:
    c = F.get_json_object(F.col("j"), "$.key")
    assert c._expr == "GET_JSON_OBJECT(`j`, '$.key')"
