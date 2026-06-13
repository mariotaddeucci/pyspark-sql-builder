from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.column import Column


def test_expr() -> None:
    c = F.expr("id + 1")
    assert isinstance(c, Column)
    assert c._expr == "id + 1"
