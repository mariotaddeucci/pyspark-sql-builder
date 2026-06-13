from __future__ import annotations

import pyarrow as pa

from pyspark_sql_builder.pyspark.sql import types


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
