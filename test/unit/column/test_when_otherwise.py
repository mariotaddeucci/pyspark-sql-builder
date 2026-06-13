from __future__ import annotations

from pyspark_sql_builder.column import Column


def test_column_when_otherwise() -> None:
    c = Column("status").when(Column("active") == True, "ativo")  # noqa: E712
    assert "CASE WHEN" in c._expr
    assert "ELSE" in c._expr
