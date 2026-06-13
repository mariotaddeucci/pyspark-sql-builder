from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import types


def test_array_type() -> None:
    t = types.ArrayType(types.StringType())
    assert t.sql() == "ARRAY<STRING>"


def test_map_type() -> None:
    t = types.MapType(types.StringType(), types.IntegerType())
    assert t.sql() == "MAP<STRING, INTEGER>"


def test_struct_type() -> None:
    fields = [
        types.StructField("name", types.StringType()),
        types.StructField("age", types.IntegerType(), nullable=False),
    ]
    t = types.StructType(fields)
    assert "STRUCT<" in t.sql()
    assert "name STRING" in t.sql()
    assert "age INTEGER NOT NULL" in t.sql()
