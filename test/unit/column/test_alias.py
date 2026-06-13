from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_column_alias() -> None:
    c = Column("salary").alias("sal")
    assert "salary AS" in c._expr
