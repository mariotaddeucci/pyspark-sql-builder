from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_like() -> None:
    c = Column("name").like("%john%")
    assert c._expr == "name LIKE '%john%'"
