from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_column_name() -> None:
    c = Column("id")
    assert c.name == "id"


def test_column_with_table() -> None:
    c = Column("users.id")
    assert c.name == "users.id"
    assert c._expr == "users.id"
