from __future__ import annotations

import pyarrow as pa

from pyspark_sql_builder import types


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
