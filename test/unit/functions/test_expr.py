from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.column import Column


def test_expr() -> None:
    c = F.expr("id + 1")
    assert isinstance(c, Column)
    assert c._expr == "id + 1"
