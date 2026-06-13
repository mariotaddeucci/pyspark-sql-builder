from __future__ import annotations

from pyspark_sql_builder.column import Column, _quote_ident, _to_expr


def _to_col(v: Column | str) -> Column:
    return col(v) if isinstance(v, str) else v


def row_number() -> Column:
    return Column("ROW_NUMBER()")


def rank() -> Column:
    return Column("RANK()")


def dense_rank() -> Column:
    return Column("DENSE_RANK()")


def lag(column: Column | str, offset: int = 1, default: object = None) -> Column:
    return Column(f"LAG({_to_expr(_to_col(column))}, {offset}, {_to_expr(default)})")


def lead(column: Column | str, offset: int = 1, default: object = None) -> Column:
    return Column(f"LEAD({_to_expr(_to_col(column))}, {offset}, {_to_expr(default)})")


def col(name: str) -> Column:
    return Column(_quote_ident(name))


def lit(value: object) -> Column:
    if isinstance(value, str):
        return Column(f"'{value}'")
    if value is None:
        return Column("NULL")
    if isinstance(value, bool):
        return Column(str(value).upper())
    return Column(str(value))


def count(column: Column | str | None = None) -> Column:
    if column is None:
        return Column("COUNT(*)")
    return Column(f"COUNT({_to_expr(_to_col(column))})")


def countDistinct(column: Column | str) -> Column:
    return Column(f"COUNT(DISTINCT {_to_expr(_to_col(column))})")


def sum(column: Column | str) -> Column:
    return Column(f"SUM({_to_expr(_to_col(column))})")


def avg(column: Column | str) -> Column:
    return Column(f"AVG({_to_expr(_to_col(column))})")


def min(column: Column | str) -> Column:
    return Column(f"MIN({_to_expr(_to_col(column))})")


def max(column: Column | str) -> Column:
    return Column(f"MAX({_to_expr(_to_col(column))})")


def coalesce(*columns: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in columns)
    return Column(f"COALESCE({args})")


def when(condition: Column, value: object) -> WhenBuilder:
    return WhenBuilder(condition, value)


class WhenBuilder:
    def __init__(self, condition: Column, value: object) -> None:
        self._conditions: list[str] = [f"WHEN {condition._expr} THEN {_to_expr(value)}"]
        self._else_value: str | None = None

    def when(self, condition: Column, value: object) -> WhenBuilder:
        self._conditions.append(f"WHEN {condition._expr} THEN {_to_expr(value)}")
        return self

    def otherwise(self, value: object) -> Column:
        clauses = " ".join(self._conditions)
        else_clause = f" ELSE {_to_expr(value)}" if value is not None else ""
        return Column(f"CASE {clauses}{else_clause} END")


def alias(column: Column | str, alias_name: str) -> Column:
    return Column(f"{_to_expr(_to_col(column))} AS `{alias_name}`")


def asc(column: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(column))} ASC")


def desc(column: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(column))} DESC")


def concat(*columns: Column | str) -> Column:
    return Column(f"CONCAT({', '.join(_to_expr(_to_col(c)) for c in columns)})")


def concat_ws(sep: str, *columns: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in columns)
    return Column(f"CONCAT_WS('{sep}', {args})")


def upper(column: Column | str) -> Column:
    return Column(f"UPPER({_to_expr(_to_col(column))})")


def lower(column: Column | str) -> Column:
    return Column(f"LOWER({_to_expr(_to_col(column))})")


def length(column: Column | str) -> Column:
    return Column(f"LENGTH({_to_expr(_to_col(column))})")


def trim(column: Column | str) -> Column:
    return Column(f"TRIM({_to_expr(_to_col(column))})")


def ltrim(column: Column | str) -> Column:
    return Column(f"LTRIM({_to_expr(_to_col(column))})")


def rtrim(column: Column | str) -> Column:
    return Column(f"RTRIM({_to_expr(_to_col(column))})")


def abs(column: Column | str) -> Column:
    return Column(f"ABS({_to_expr(_to_col(column))})")


def ceil(column: Column | str) -> Column:
    return Column(f"CEIL({_to_expr(_to_col(column))})")


def floor(column: Column | str) -> Column:
    return Column(f"FLOOR({_to_expr(_to_col(column))})")


def round(column: Column | str, scale: int = 0) -> Column:
    return Column(f"ROUND({_to_expr(_to_col(column))}, {scale})")


def sqrt(column: Column | str) -> Column:
    return Column(f"SQRT({_to_expr(_to_col(column))})")


def power(column: Column | str, exponent: object) -> Column:
    return Column(f"POWER({_to_expr(_to_col(column))}, {_to_expr(exponent)})")


def exp(column: Column | str) -> Column:
    return Column(f"EXP({_to_expr(_to_col(column))})")


def log(column: Column | str) -> Column:
    return Column(f"LOG({_to_expr(_to_col(column))})")


def current_date() -> Column:
    return Column("CURRENT_DATE")


def current_timestamp() -> Column:
    return Column("CURRENT_TIMESTAMP")


def date_add(column: Column | str, days: int) -> Column:
    return Column(f"DATE_ADD({_to_expr(_to_col(column))}, {days})")


def date_sub(column: Column | str, days: int) -> Column:
    return Column(f"DATE_SUB({_to_expr(_to_col(column))}, {days})")


def datediff(end: Column | str, start: Column | str) -> Column:
    return Column(f"DATEDIFF({_to_expr(_to_col(end))}, {_to_expr(_to_col(start))})")


def year(column: Column | str) -> Column:
    return Column(f"YEAR({_to_expr(_to_col(column))})")


def month(column: Column | str) -> Column:
    return Column(f"MONTH({_to_expr(_to_col(column))})")


def day(column: Column | str) -> Column:
    return Column(f"DAY({_to_expr(_to_col(column))})")


def hour(column: Column | str) -> Column:
    return Column(f"HOUR({_to_expr(_to_col(column))})")


def minute(column: Column | str) -> Column:
    return Column(f"MINUTE({_to_expr(_to_col(column))})")


def second(column: Column | str) -> Column:
    return Column(f"SECOND({_to_expr(_to_col(column))})")


def unix_timestamp(column: Column | str | None = None) -> Column:
    if column is None:
        return Column("UNIX_TIMESTAMP()")
    return Column(f"UNIX_TIMESTAMP({_to_expr(_to_col(column))})")


def from_unixtime(column: Column | str, fmt: str = "yyyy-MM-dd HH:mm:ss") -> Column:
    return Column(f"FROM_UNIXTIME({_to_expr(_to_col(column))}, '{fmt}')")


def format_number(column: Column | str, decimal_places: int) -> Column:
    return Column(f"FORMAT_NUMBER({_to_expr(_to_col(column))}, {decimal_places})")


def initcap(column: Column | str) -> Column:
    return Column(f"INITCAP({_to_expr(_to_col(column))})")


def reverse(column: Column | str) -> Column:
    return Column(f"REVERSE({_to_expr(_to_col(column))})")


def replace(column: Column | str, search: str, replace_str: str = "") -> Column:
    return Column(f"REPLACE({_to_expr(_to_col(column))}, '{search}', '{replace_str}')")


def substring(column: Column | str, pos: int, length: int | None = None) -> Column:
    if length is not None:
        return Column(f"SUBSTRING({_to_expr(_to_col(column))}, {pos}, {length})")
    return Column(f"SUBSTRING({_to_expr(_to_col(column))}, {pos})")


def split(column: Column | str, pattern: str) -> Column:
    return Column(f"SPLIT({_to_expr(_to_col(column))}, '{pattern}')")
