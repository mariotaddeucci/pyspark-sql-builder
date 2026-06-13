from __future__ import annotations

from pyspark_sql_builder import types


def test_string_type() -> None:
    t = types.StringType()
    assert t.sql() == "STRING"


def test_integer_type() -> None:
    t = types.IntegerType()
    assert t.sql() == "INTEGER"


def test_long_type() -> None:
    t = types.LongType()
    assert t.sql() == "BIGINT"


def test_float_type() -> None:
    t = types.FloatType()
    assert t.sql() == "FLOAT"


def test_double_type() -> None:
    t = types.DoubleType()
    assert t.sql() == "DOUBLE"


def test_boolean_type() -> None:
    t = types.BooleanType()
    assert t.sql() == "BOOLEAN"


def test_date_type() -> None:
    t = types.DateType()
    assert t.sql() == "DATE"


def test_timestamp_type() -> None:
    t = types.TimestampType()
    assert t.sql() == "TIMESTAMP"


def test_decimal_type() -> None:
    t = types.DecimalType(10, 2)
    assert t.sql() == "DECIMAL(10, 2)"


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


def test_binary_type() -> None:
    t = types.BinaryType()
    assert t.sql() == "BINARY"
