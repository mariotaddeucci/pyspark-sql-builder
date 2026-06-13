from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_and() -> None:
    c = (Column("age") > 18) & (Column("age") < 65)
    assert "(age > 18 AND age < 65)" in c._expr


def test_or() -> None:
    c = (Column("status") == "active") | (Column("status") == "pending")
    assert "status = 'active' OR status = 'pending'" in c._expr


def test_invert() -> None:
    c = ~(Column("age") > 18)
    assert "NOT" in c._expr
