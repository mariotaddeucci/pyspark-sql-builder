from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import types


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


def test_binary_type() -> None:
    t = types.BinaryType()
    assert t.sql() == "BINARY"


def test_decimal_type() -> None:
    t = types.DecimalType(10, 2)
    assert t.sql() == "DECIMAL(10, 2)"
