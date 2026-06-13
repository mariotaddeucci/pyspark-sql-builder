from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_element_at() -> None:
    c = F.element_at(F.col("a"), 1)
    assert c._expr == "ELEMENT_AT(`a`, 1)"
