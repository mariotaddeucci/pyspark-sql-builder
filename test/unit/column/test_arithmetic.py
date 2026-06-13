from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_arithmetic() -> None:
    assert (Column("a") + Column("b"))._expr == "a + b"
    assert (Column("a") - Column("b"))._expr == "a - b"
    assert (Column("a") * Column("b"))._expr == "a * b"
    assert (Column("a") / Column("b"))._expr == "a / b"
