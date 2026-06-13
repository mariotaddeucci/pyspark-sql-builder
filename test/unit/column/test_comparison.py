from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_eq() -> None:
    c = Column("age") == 18
    assert c._expr == "age = 18"


def test_eq_column() -> None:
    c = Column("a") == Column("b")
    assert c._expr == "a = b"


def test_neq() -> None:
    c = Column("status") != "active"
    assert c._expr == "status != 'active'"


def test_gt() -> None:
    c = Column("age") > 21
    assert c._expr == "age > 21"


def test_ge() -> None:
    c = Column("age") >= 18
    assert c._expr == "age >= 18"


def test_lt() -> None:
    c = Column("age") < 65
    assert c._expr == "age < 65"


def test_le() -> None:
    c = Column("age") <= 60
    assert c._expr == "age <= 60"
