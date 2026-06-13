from __future__ import annotations


class DataType:
    def __init__(self, sql_type: str) -> None:
        self._sql_type = sql_type

    def __repr__(self) -> str:
        return f"DataType('{self._sql_type}')"

    def sql(self) -> str:
        return self._sql_type


class StringType(DataType):
    def __init__(self) -> None:
        super().__init__("STRING")


class IntegerType(DataType):
    def __init__(self) -> None:
        super().__init__("INTEGER")


class LongType(DataType):
    def __init__(self) -> None:
        super().__init__("BIGINT")


class FloatType(DataType):
    def __init__(self) -> None:
        super().__init__("FLOAT")


class DoubleType(DataType):
    def __init__(self) -> None:
        super().__init__("DOUBLE")


class BooleanType(DataType):
    def __init__(self) -> None:
        super().__init__("BOOLEAN")


class DateType(DataType):
    def __init__(self) -> None:
        super().__init__("DATE")


class TimestampType(DataType):
    def __init__(self) -> None:
        super().__init__("TIMESTAMP")


class BinaryType(DataType):
    def __init__(self) -> None:
        super().__init__("BINARY")


class ArrayType(DataType):
    def __init__(self, element_type: DataType) -> None:
        super().__init__(f"ARRAY<{element_type.sql()}>")


class MapType(DataType):
    def __init__(self, key_type: DataType, value_type: DataType) -> None:
        super().__init__(f"MAP<{key_type.sql()}, {value_type.sql()}>")


class StructField:
    def __init__(self, name: str, data_type: DataType, nullable: bool = True) -> None:
        self.name = name
        self.data_type = data_type
        self.nullable = nullable


class StructType(DataType):
    def __init__(self, fields: list[StructField] | None = None) -> None:
        if fields:
            cols = ", ".join(
                f"{f.name} {f.data_type.sql()}" + ("" if f.nullable else " NOT NULL")
                for f in fields
            )
            super().__init__(f"STRUCT<{cols}>")
        else:
            super().__init__("STRUCT<>")


class DecimalType(DataType):
    def __init__(self, precision: int = 10, scale: int = 0) -> None:
        super().__init__(f"DECIMAL({precision}, {scale})")
