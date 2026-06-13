from __future__ import annotations

import pyarrow as pa
import pyarrow.types as pat


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
