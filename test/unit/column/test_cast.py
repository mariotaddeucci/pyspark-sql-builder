from __future__ import annotations

from pyspark_sql_builder.pyspark.sql.column import Column


def test_cast() -> None:
    c = Column("age").cast("STRING")
    assert c._expr == "CAST(age AS STRING)"
