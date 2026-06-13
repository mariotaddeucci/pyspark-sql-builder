from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_asc() -> None:
    c = Column("name").asc()
    assert c._expr == "name ASC"


def test_desc() -> None:
    c = Column("name").desc()
    assert c._expr == "name DESC"
