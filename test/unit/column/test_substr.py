from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_substr() -> None:
    c = Column("name").substr(1, 3)
    assert c._expr == "SUBSTRING(name, 1, 3)"
