from __future__ import annotations

from pyspark_sql_builder.column import Column, _quote_ident, _to_expr


def row_number() -> Column:
    return Column("ROW_NUMBER()")


def rank() -> Column:
    return Column("RANK()")


def dense_rank() -> Column:
    return Column("DENSE_RANK()")


def lag(column: Column | str, offset: int = 1, default: object = None) -> Column:
    return Column(f"LAG({_to_expr(column)}, {offset}, {_to_expr(default)})")


def lead(column: Column | str, offset: int = 1, default: object = None) -> Column:
    return Column(f"LEAD({_to_expr(column)}, {offset}, {_to_expr(default)})")




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
    return Column(f"COUNT({_to_expr(column)})")


def countDistinct(column: Column | str) -> Column:
    return Column(f"COUNT(DISTINCT {_to_expr(column)})")


def sum(column: Column | str) -> Column:
    return Column(f"SUM({_to_expr(column)})")


def avg(column: Column | str) -> Column:
    return Column(f"AVG({_to_expr(column)})")


def min(column: Column | str) -> Column:
    return Column(f"MIN({_to_expr(column)})")


def max(column: Column | str) -> Column:
    return Column(f"MAX({_to_expr(column)})")


def coalesce(*columns: Column | str) -> Column:
    args = ", ".join(_to_expr(c) for c in columns)
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
    return Column(f"{_to_expr(column)} AS `{alias_name}`")


def asc(column: Column | str) -> Column:
    return Column(f"{_to_expr(column)} ASC")


def desc(column: Column | str) -> Column:
    return Column(f"{_to_expr(column)} DESC")


def concat(*columns: Column | str) -> Column:
    return Column(f"CONCAT({', '.join(_to_expr(c) for c in columns)})")


def concat_ws(sep: str, *columns: Column | str) -> Column:
    return Column(f"CONCAT_WS('{sep}', {', '.join(_to_expr(c) for c in columns)})")


def upper(column: Column | str) -> Column:
    return Column(f"UPPER({_to_expr(column)})")


def lower(column: Column | str) -> Column:
    return Column(f"LOWER({_to_expr(column)})")


def length(column: Column | str) -> Column:
    return Column(f"LENGTH({_to_expr(column)})")


def trim(column: Column | str) -> Column:
    return Column(f"TRIM({_to_expr(column)})")


def ltrim(column: Column | str) -> Column:
    return Column(f"LTRIM({_to_expr(column)})")


def rtrim(column: Column | str) -> Column:
    return Column(f"RTRIM({_to_expr(column)})")


def abs(column: Column | str) -> Column:
    return Column(f"ABS({_to_expr(column)})")


def ceil(column: Column | str) -> Column:
    return Column(f"CEIL({_to_expr(column)})")


def floor(column: Column | str) -> Column:
    return Column(f"FLOOR({_to_expr(column)})")


def round(column: Column | str, scale: int = 0) -> Column:
    return Column(f"ROUND({_to_expr(column)}, {scale})")


def sqrt(column: Column | str) -> Column:
    return Column(f"SQRT({_to_expr(column)})")


def power(column: Column | str, exponent: object) -> Column:
    return Column(f"POWER({_to_expr(column)}, {_to_expr(exponent)})")


def exp(column: Column | str) -> Column:
    return Column(f"EXP({_to_expr(column)})")


def log(column: Column | str) -> Column:
    return Column(f"LOG({_to_expr(column)})")


def current_date() -> Column:
    return Column("CURRENT_DATE")


def current_timestamp() -> Column:
    return Column("CURRENT_TIMESTAMP")


def date_add(column: Column | str, days: int) -> Column:
    return Column(f"DATE_ADD({_to_expr(column)}, {days})")


def date_sub(column: Column | str, days: int) -> Column:
    return Column(f"DATE_SUB({_to_expr(column)}, {days})")


def datediff(end: Column | str, start: Column | str) -> Column:
    return Column(f"DATEDIFF({_to_expr(end)}, {_to_expr(start)})")


def year(column: Column | str) -> Column:
    return Column(f"YEAR({_to_expr(column)})")


def month(column: Column | str) -> Column:
    return Column(f"MONTH({_to_expr(column)})")


def day(column: Column | str) -> Column:
    return Column(f"DAY({_to_expr(column)})")


def hour(column: Column | str) -> Column:
    return Column(f"HOUR({_to_expr(column)})")


def minute(column: Column | str) -> Column:
    return Column(f"MINUTE({_to_expr(column)})")


def second(column: Column | str) -> Column:
    return Column(f"SECOND({_to_expr(column)})")


def unix_timestamp(column: Column | str | None = None) -> Column:
    if column is None:
        return Column("UNIX_TIMESTAMP()")
    return Column(f"UNIX_TIMESTAMP({_to_expr(column)})")


def from_unixtime(column: Column | str, fmt: str = "yyyy-MM-dd HH:mm:ss") -> Column:
    return Column(f"FROM_UNIXTIME({_to_expr(column)}, '{fmt}')")


def format_number(column: Column | str, decimal_places: int) -> Column:
    return Column(f"FORMAT_NUMBER({_to_expr(column)}, {decimal_places})")


def initcap(column: Column | str) -> Column:
    return Column(f"INITCAP({_to_expr(column)})")


def reverse(column: Column | str) -> Column:
    return Column(f"REVERSE({_to_expr(column)})")


def replace(column: Column | str, search: str, replace_str: str = "") -> Column:
    return Column(f"REPLACE({_to_expr(column)}, '{search}', '{replace_str}')")


def substring(column: Column | str, pos: int, length: int | None = None) -> Column:
    if length is not None:
        return Column(f"SUBSTRING({_to_expr(column)}, {pos}, {length})")
    return Column(f"SUBSTRING({_to_expr(column)}, {pos})")


def split(column: Column | str, pattern: str) -> Column:
    return Column(f"SPLIT({_to_expr(column)}, '{pattern}')")



