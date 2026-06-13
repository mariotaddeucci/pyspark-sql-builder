from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_substr() -> None:
    c = Column("name").substr(1, 3)
    assert c._expr == "SUBSTRING(name, 1, 3)"
