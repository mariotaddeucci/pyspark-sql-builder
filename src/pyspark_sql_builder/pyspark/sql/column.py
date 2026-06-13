from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark_sql_builder.pyspark.sql.window import Window


def _quote_ident(name: str) -> str:
    if name == "*":
        return name
    parts = name.split(".")
    return ".".join(f"`{p}`" if p != "*" else p for p in parts)


class Column:
    def __init__(self, expr: str) -> None:
        self._expr = expr

    @property
    def name(self) -> str:
        parts = self._expr.split(".")
        return ".".join(p.strip("`") for p in parts)

    def alias(self, alias: str) -> Column:
        return Column(f"{self._expr} AS `{alias}`")

    def asc(self) -> Column:
        return Column(f"{self._expr} ASC")

    def desc(self) -> Column:
        return Column(f"{self._expr} DESC")

    def cast(self, data_type: str) -> Column:
        return Column(f"CAST({self._expr} AS {data_type})")

    def isNull(self) -> Column:
        return Column(f"{self._expr} IS NULL")

    def isNotNull(self) -> Column:
        return Column(f"{self._expr} IS NOT NULL")

    def between(self, low: object, high: object) -> Column:
        return Column(f"{self._expr} BETWEEN {_to_expr(low)} AND {_to_expr(high)}")

    def like(self, pattern: object) -> Column:
        return Column(f"{self._expr} LIKE {_to_expr(pattern)}")

    def startswith(self, other: object) -> Column:
        return Column(f"{self._expr} LIKE {_to_expr(other)} || '%'")

    def endswith(self, other: object) -> Column:
        return Column(f"{self._expr} LIKE '%' || {_to_expr(other)}")

    def contains(self, other: object) -> Column:
        return Column(f"{self._expr} LIKE '%' || {_to_expr(other)} || '%'")

    def substr(self, start: int, length: int | None = None) -> Column:
        if length is not None:
            return Column(f"SUBSTRING({self._expr}, {start}, {length})")
        return Column(f"SUBSTRING({self._expr}, {start})")

    def when(self, condition: Column, value: object) -> Column:
        cond_s = condition._expr
        val_s = _to_expr(value)
        return Column(f"CASE WHEN {cond_s} THEN {val_s} ELSE {self._expr} END")

    def otherwise(self, value: object) -> Column:
        return Column(f"COALESCE({self._expr}, {_to_expr(value)})")

    def over(self, window: Window) -> Column:
        return Column(f"{self._expr} OVER ({window._spec_sql()})")

    def _expr_sql(self) -> str:
        return self._expr

    def __eq__(self, other: object) -> Column:  # type: ignore[override]
        return Column(f"{self._expr} = {_to_expr(other)}")

    def __ne__(self, other: object) -> Column:  # type: ignore[override]
        return Column(f"{self._expr} != {_to_expr(other)}")

    def __gt__(self, other: object) -> Column:
        return Column(f"{self._expr} > {_to_expr(other)}")

    def __ge__(self, other: object) -> Column:
        return Column(f"{self._expr} >= {_to_expr(other)}")

    def __lt__(self, other: object) -> Column:
        return Column(f"{self._expr} < {_to_expr(other)}")

    def __le__(self, other: object) -> Column:
        return Column(f"{self._expr} <= {_to_expr(other)}")

    def __and__(self, other: object) -> Column:
        return Column(f"({self._expr} AND {_to_expr(other)})")

    def __or__(self, other: object) -> Column:
        return Column(f"({self._expr} OR {_to_expr(other)})")

    def __add__(self, other: object) -> Column:
        return Column(f"{self._expr} + {_to_expr(other)}")

    def __sub__(self, other: object) -> Column:
        return Column(f"{self._expr} - {_to_expr(other)}")

    def __mul__(self, other: object) -> Column:
        return Column(f"{self._expr} * {_to_expr(other)}")

    def __truediv__(self, other: object) -> Column:
        return Column(f"{self._expr} / {_to_expr(other)}")

    def __mod__(self, other: object) -> Column:
        return Column(f"{self._expr} % {_to_expr(other)}")

    def __invert__(self) -> Column:
        return Column(f"NOT ({self._expr})")

    def __hash__(self) -> int:
        return hash(self._expr)

    def __repr__(self) -> str:
        return f"Column('{self._expr}')"


def _to_expr(value: object) -> str:
    if isinstance(value, Column):
        return value._expr
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return str(value).upper()
    return str(value)
