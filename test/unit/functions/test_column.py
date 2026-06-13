from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.column import Column


def test_column() -> None:
    c = F.column("id")
    assert isinstance(c, Column)
    assert c._expr == "`id`"


def test_column_dotted() -> None:
    c = F.column("t.id")
    assert c._expr == "`t`.`id`"
