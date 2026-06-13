from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_from_json() -> None:
    c = F.from_json(F.col("val"), "a INT")
    assert c._expr == "FROM_JSON(`val`, 'a INT')"
