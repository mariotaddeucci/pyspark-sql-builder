from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pyarrow as pa
import pyarrow.types as pat


class Row:
    """Represents a row in a DataFrame.

    A Row object is immutable and acts like a named tuple, allowing access
    to values by column name (as attribute) or by index/column name (as item).

    Example:
        >>> row = Row(name="Alice", age=30)
        >>> row.name
        'Alice'
        >>> row["name"]
        'Alice'
        >>> row[0]
        'Alice'
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a Row.

        Args:
            *args: Positional values (stored by index)
            **kwargs: Named values (accessed by name)
        """
        if args and kwargs:
            raise ValueError("Cannot specify both positional and keyword arguments")

        if args:
            self._values = args
            self._fields = tuple(f"_{i}" for i in range(len(args)))
        else:
            self._fields = tuple(sorted(kwargs.keys()))
            self._values = tuple(kwargs[k] for k in self._fields)

    def __getitem__(self, key: int | str) -> Any:
        """Access value by index or field name."""
        if isinstance(key, int):
            return self._values[key]
        if isinstance(key, str):
            try:
                idx = self._fields.index(key)
                return self._values[idx]
            except ValueError:
                raise KeyError(f"Column '{key}' not found in Row")
        raise TypeError(
            f"indices must be integers or strings, not {type(key).__name__}"
        )

    def __getattr__(self, name: str) -> Any:
        """Access value by attribute name."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
        try:
            idx = self._fields.index(name)
            return self._values[idx]
        except ValueError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

    def __repr__(self) -> str:
        if self._fields and not all(f.startswith("_") for f in self._fields):
            items = ", ".join(f"{k}={v!r}" for k, v in zip(self._fields, self._values))
            return f"Row({items})"
        return f"Row({', '.join(repr(v) for v in self._values)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Row):
            return NotImplemented
        return self._values == other._values and self._fields == other._fields

    def __hash__(self) -> int:
        return hash((self._values, self._fields))

    def __len__(self) -> int:
        """Return the number of fields in the Row."""
        return len(self._values)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over values in the Row."""
        return iter(self._values)

    def asDict(self, recursive: bool = False) -> dict[str, Any]:  # noqa: N802
        """Convert Row to a dictionary.

        Args:
            recursive: If True, recursively convert nested Rows to dicts.

        Returns:
            Dictionary representation of the Row.
        """
        result: dict[str, Any] = {}
        for k, v in zip(self._fields, self._values):
            if recursive and isinstance(v, Row):
                result[k] = v.asDict(recursive=True)
            elif recursive and isinstance(v, (list, tuple)):
                result[k] = [
                    item.asDict(recursive=True) if isinstance(item, Row) else item
                    for item in v
                ]
            else:
                result[k] = v
        return result


class DataType:
    def __init__(self, sql_type: str) -> None:
        self._sql_type = sql_type

    def __repr__(self) -> str:
        return f"DataType('{self._sql_type}')"

    def sql(self) -> str:
        return self._sql_type

    def simpleString(self) -> str:
        return self._sql_type

    def typeName(self) -> str:
        return type(self).__name__.replace("Type", "").lower()

    def needConversion(self) -> bool:
        return False


class StringType(DataType):
    def __init__(self) -> None:
        super().__init__("STRING")

    def simpleString(self) -> str:
        return "string"


class IntegerType(DataType):
    def __init__(self) -> None:
        super().__init__("INTEGER")

    def simpleString(self) -> str:
        return "int"


class LongType(DataType):
    def __init__(self) -> None:
        super().__init__("BIGINT")

    def simpleString(self) -> str:
        return "bigint"


class FloatType(DataType):
    def __init__(self) -> None:
        super().__init__("FLOAT")

    def simpleString(self) -> str:
        return "float"


class DoubleType(DataType):
    def __init__(self) -> None:
        super().__init__("DOUBLE")

    def simpleString(self) -> str:
        return "double"


class BooleanType(DataType):
    def __init__(self) -> None:
        super().__init__("BOOLEAN")

    def simpleString(self) -> str:
        return "boolean"


class DateType(DataType):
    def __init__(self) -> None:
        super().__init__("DATE")

    def simpleString(self) -> str:
        return "date"


class TimestampType(DataType):
    def __init__(self) -> None:
        super().__init__("TIMESTAMP")

    def simpleString(self) -> str:
        return "timestamp"


class BinaryType(DataType):
    def __init__(self) -> None:
        super().__init__("BINARY")

    def simpleString(self) -> str:
        return "binary"


class ArrayType(DataType):
    def __init__(self, element_type: DataType, contains_null: bool = True) -> None:
        self.element_type = element_type
        self.contains_null = contains_null
        super().__init__(f"ARRAY<{element_type.sql()}>")

    def simpleString(self) -> str:
        return f"array<{self.element_type.simpleString()}>"


class MapType(DataType):
    def __init__(
        self,
        key_type: DataType,
        value_type: DataType,
        value_contains_null: bool = True,
    ) -> None:
        self.key_type = key_type
        self.value_type = value_type
        self.value_contains_null = value_contains_null
        super().__init__(f"MAP<{key_type.sql()}, {value_type.sql()}>")

    def simpleString(self) -> str:
        return f"map<{self.key_type.simpleString()},{self.value_type.simpleString()}>"


class StructField:
    def __init__(self, name: str, data_type: DataType, nullable: bool = True) -> None:
        self.name = name
        self.data_type = data_type
        self.nullable = nullable

    def simpleString(self) -> str:
        return f"{self.name}: {self.data_type.simpleString()}"


class StructType(DataType):
    def __init__(self, fields: list[StructField] | None = None) -> None:
        self.fields = fields or []
        cols = ", ".join(
            f"{f.name} {f.data_type.sql()}" + ("" if f.nullable else " NOT NULL")
            for f in self.fields
        )
        super().__init__(f"STRUCT<{cols}>" if cols else "STRUCT<>")

    def simpleString(self) -> str:
        inner = ", ".join(f.simpleString() for f in self.fields)
        return f"struct<{inner}>"


class DecimalType(DataType):
    def __init__(self, precision: int = 10, scale: int = 0) -> None:
        self.precision = precision
        self.scale = scale
        super().__init__(f"DECIMAL({precision}, {scale})")

    def simpleString(self) -> str:
        return f"decimal({self.precision},{self.scale})"


def _arrow_to_spark_type(t: pa.DataType) -> DataType:
    if pat.is_int32(t):
        return IntegerType()
    if pat.is_int64(t):
        return LongType()
    if pat.is_float32(t):
        return FloatType()
    if pat.is_float64(t):
        return DoubleType()
    if pat.is_string(t) or pat.is_large_string(t):
        return StringType()
    if pat.is_boolean(t):
        return BooleanType()
    if pat.is_date(t):
        return DateType()
    if pat.is_timestamp(t):
        return TimestampType()
    if pat.is_binary(t) or pat.is_large_binary(t):
        return BinaryType()
    if pat.is_decimal(t):
        return DecimalType(t.precision, t.scale)
    if pat.is_list(t) or pat.is_large_list(t):
        element = _arrow_to_spark_type(t.value_type)
        return ArrayType(element, t.value_field.nullable)
    if pat.is_map(t):
        key = _arrow_to_spark_type(t.key_type)
        value = _arrow_to_spark_type(t.item_type)
        return MapType(key, value, t.item_field.nullable)
    if pat.is_struct(t):
        fields = [
            StructField(f.name, _arrow_to_spark_type(f.type), f.nullable) for f in t
        ]
        return StructType(fields)
    return DataType(str(t))


def _arrow_to_dtype_string(t: pa.DataType) -> str:
    return _arrow_to_spark_type(t).simpleString()


def _print_schema_field(field: pa.Field, indent: int = 0) -> None:
    prefix = " " * indent + " |-- " if indent else ""
    t = field.type
    spark_type = _arrow_to_spark_type(t)
    type_name = spark_type.typeName()

    if isinstance(spark_type, StructType):
        print(f"{prefix}{field.name}: {type_name} (nullable = {field.nullable})")
        for f in t:
            _print_schema_field(f, indent + 3)
    elif isinstance(spark_type, ArrayType):
        print(f"{prefix}{field.name}: {type_name} (nullable = {field.nullable})")
        elem_prefix = " " * (indent + 3) + " |-- "
        print(
            f"{elem_prefix}element: {_arrow_to_spark_type(t.value_type).typeName()}"
            f" (containsNull = {t.value_field.nullable})"
        )
    elif isinstance(spark_type, MapType):
        print(f"{prefix}{field.name}: {type_name} (nullable = {field.nullable})")
        inner_prefix = " " * (indent + 3) + " |-- "
        print(f"{inner_prefix}key: {_arrow_to_spark_type(t.key_type).typeName()}")
        print(
            f"{inner_prefix}value: {_arrow_to_spark_type(t.item_type).typeName()}"
            f" (valueContainsNull = {t.item_field.nullable})"
        )
    else:
        print(f"{prefix}{field.name}: {type_name} (nullable = {field.nullable})")


def _arrow_schema_to_struct_type(schema: pa.Schema) -> StructType:
    fields = [
        StructField(f.name, _arrow_to_spark_type(f.type), f.nullable) for f in schema
    ]
    return StructType(fields)
