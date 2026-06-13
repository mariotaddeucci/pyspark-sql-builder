from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_is_null() -> None:
    c = Column("email").isNull()
    assert c._expr == "email IS NULL"


def test_is_not_null() -> None:
    c = Column("email").isNotNull()
    assert c._expr == "email IS NOT NULL"
