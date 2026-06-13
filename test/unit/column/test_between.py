from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_between() -> None:
    c = Column("age").between(18, 65)
    assert c._expr == "age BETWEEN 18 AND 65"
