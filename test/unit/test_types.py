from __future__ import annotations

import pyarrow as pa

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


def test_arrow_to_spark_type_int32() -> None:
    t = types._arrow_to_spark_type(pa.int32())
    assert isinstance(t, types.IntegerType)


def test_arrow_to_spark_type_int64() -> None:
    t = types._arrow_to_spark_type(pa.int64())
    assert isinstance(t, types.LongType)


def test_arrow_to_spark_type_float() -> None:
    t = types._arrow_to_spark_type(pa.float32())
    assert isinstance(t, types.FloatType)


def test_arrow_to_spark_type_double() -> None:
    t = types._arrow_to_spark_type(pa.float64())
    assert isinstance(t, types.DoubleType)


def test_arrow_to_spark_type_string() -> None:
    t = types._arrow_to_spark_type(pa.string())
    assert isinstance(t, types.StringType)


def test_arrow_to_spark_type_bool() -> None:
    t = types._arrow_to_spark_type(pa.bool_())
    assert isinstance(t, types.BooleanType)


def test_arrow_to_spark_type_date() -> None:
    t = types._arrow_to_spark_type(pa.date32())
    assert isinstance(t, types.DateType)


def test_arrow_to_spark_type_timestamp() -> None:
    t = types._arrow_to_spark_type(pa.timestamp("s"))
    assert isinstance(t, types.TimestampType)


def test_arrow_to_spark_type_binary() -> None:
    t = types._arrow_to_spark_type(pa.binary())
    assert isinstance(t, types.BinaryType)


def test_arrow_to_spark_type_decimal() -> None:
    t = types._arrow_to_spark_type(pa.decimal128(10, 2))
    assert isinstance(t, types.DecimalType)
    assert t.precision == 10
    assert t.scale == 2


def test_arrow_to_spark_type_list() -> None:
    t = types._arrow_to_spark_type(pa.list_(pa.int32()))
    assert isinstance(t, types.ArrayType)
    assert isinstance(t.element_type, types.IntegerType)


def test_arrow_to_spark_type_map() -> None:
    t = types._arrow_to_spark_type(pa.map_(pa.string(), pa.int32()))
    assert isinstance(t, types.MapType)
    assert isinstance(t.key_type, types.StringType)
    assert isinstance(t.value_type, types.IntegerType)


def test_arrow_to_spark_type_struct() -> None:
    t = types._arrow_to_spark_type(
        pa.struct([pa.field("a", pa.int32()), pa.field("b", pa.string())])
    )
    assert isinstance(t, types.StructType)
    assert len(t.fields) == 2
    assert t.fields[0].name == "a"
    assert isinstance(t.fields[0].data_type, types.IntegerType)
    assert t.fields[1].name == "b"
    assert isinstance(t.fields[1].data_type, types.StringType)


def test_arrow_to_dtype_string_scalars() -> None:
    assert types._arrow_to_dtype_string(pa.int32()) == "int"
    assert types._arrow_to_dtype_string(pa.int64()) == "bigint"
    assert types._arrow_to_dtype_string(pa.float32()) == "float"
    assert types._arrow_to_dtype_string(pa.float64()) == "double"
    assert types._arrow_to_dtype_string(pa.string()) == "string"
    assert types._arrow_to_dtype_string(pa.bool_()) == "boolean"
    assert types._arrow_to_dtype_string(pa.date32()) == "date"
    assert types._arrow_to_dtype_string(pa.timestamp("s")) == "timestamp"
    assert types._arrow_to_dtype_string(pa.binary()) == "binary"
    assert types._arrow_to_dtype_string(pa.decimal128(10, 2)) == "decimal(10,2)"


def test_arrow_to_dtype_string_nested() -> None:
    assert types._arrow_to_dtype_string(pa.list_(pa.int32())) == "array<int>"
    assert (
        types._arrow_to_dtype_string(pa.map_(pa.string(), pa.int32()))
        == "map<string,int>"
    )
    result = types._arrow_to_dtype_string(pa.struct([pa.field("a", pa.int32())]))
    assert result == "struct<a: int>"
