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


def column(name: str) -> Column:
    return Column(_quote_ident(name))


def expr(str_expr: str) -> Column:
    return Column(str_expr)


def broadcast(df: object) -> Column:
    raise NotImplementedError("broadcast is not supported in SQL mode")


def call_function(name: str, *args: object) -> Column:
    args_str = ", ".join(_to_expr(a) for a in args)
    return Column(f"{name}({args_str})")


def ifnull(col: Column | str, alt: object) -> Column:
    return Column(f"IFNULL({_to_expr(_to_col(col))}, {_to_expr(alt)})")


def nanvl(col: Column | str, alt: object) -> Column:
    c = _to_expr(_to_col(col))
    return Column(f"IF(ISNAN({c}), {_to_expr(alt)}, {c})")


def nullif(col: Column | str, val: object) -> Column:
    return Column(f"NULLIF({_to_expr(_to_col(col))}, {_to_expr(val)})")


def nullifzero(col: Column | str) -> Column:
    return Column(f"NULLIF({_to_expr(_to_col(col))}, 0)")


def nvl(col: Column | str, alt: object) -> Column:
    return Column(f"NVL({_to_expr(_to_col(col))}, {_to_expr(alt)})")


def nvl2(col: Column | str, v1: object, v2: object) -> Column:
    c = _to_expr(_to_col(col))
    v1_expr = _to_expr(v1)
    v2_expr = _to_expr(v2)
    return Column(f"CASE WHEN {c} IS NOT NULL THEN {v1_expr} ELSE {v2_expr} END")


def zeroifnull(col: Column | str) -> Column:
    return Column(f"COALESCE({_to_expr(_to_col(col))}, 0)")


def equal_null(col1: Column | str, col2: object) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} <=> {_to_expr(col2)}")


def ilike(col: Column | str, pattern: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} ILIKE '{pattern}'")


def isnan(col: Column | str) -> Column:
    return Column(f"ISNAN({_to_expr(_to_col(col))})")


def isnotnull(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} IS NOT NULL")


def isnull(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} IS NULL")


def like(col: Column | str, pattern: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} LIKE '{pattern}'")


def regexp(col: Column | str, regex: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} RLIKE '{regex}'")


def regexp_like(col: Column | str, regex: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} RLIKE '{regex}'")


def rlike(col: Column | str, regex: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} RLIKE '{regex}'")


def asc_nulls_first(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} ASC NULLS FIRST")


def asc_nulls_last(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} ASC NULLS LAST")


def desc_nulls_first(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} DESC NULLS FIRST")


def desc_nulls_last(col: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} DESC NULLS LAST")


# ── Math functions ──────────────────────────────────────────────────────


def acos(col: Column | str) -> Column:
    return Column(f"ACOS({_to_expr(_to_col(col))})")


def acosh(col: Column | str) -> Column:
    return Column(f"ACOSH({_to_expr(_to_col(col))})")


def asin(col: Column | str) -> Column:
    return Column(f"ASIN({_to_expr(_to_col(col))})")


def asinh(col: Column | str) -> Column:
    return Column(f"ASINH({_to_expr(_to_col(col))})")


def atan(col: Column | str) -> Column:
    return Column(f"ATAN({_to_expr(_to_col(col))})")


def atan2(colY: Column | str, colX: Column | str) -> Column:
    return Column(f"ATAN2({_to_expr(_to_col(colY))}, {_to_expr(_to_col(colX))})")


def atanh(col: Column | str) -> Column:
    return Column(f"ATANH({_to_expr(_to_col(col))})")


def bin(col: Column | str) -> Column:
    return Column(f"BIN({_to_expr(_to_col(col))})")


def bround(col: Column | str, scale: int = 0) -> Column:
    return Column(f"BROUND({_to_expr(_to_col(col))}, {scale})")


def cbrt(col: Column | str) -> Column:
    return Column(f"CBRT({_to_expr(_to_col(col))})")


def ceiling(col: Column | str) -> Column:
    return Column(f"CEIL({_to_expr(_to_col(col))})")


def conv(col: Column | str, fromBase: int, toBase: int) -> Column:
    return Column(f"CONV({_to_expr(_to_col(col))}, {fromBase}, {toBase})")


def cos(col: Column | str) -> Column:
    return Column(f"COS({_to_expr(_to_col(col))})")


def cosh(col: Column | str) -> Column:
    return Column(f"COSH({_to_expr(_to_col(col))})")


def cot(col: Column | str) -> Column:
    return Column(f"COT({_to_expr(_to_col(col))})")


def csc(col: Column | str) -> Column:
    return Column(f"CSC({_to_expr(_to_col(col))})")


def degrees(col: Column | str) -> Column:
    return Column(f"DEGREES({_to_expr(_to_col(col))})")


def e() -> Column:
    return Column("E()")


def expm1(col: Column | str) -> Column:
    return Column(f"EXP({_to_expr(_to_col(col))}) - 1")


def factorial(col: Column | str) -> Column:
    return Column(f"FACTORIAL({_to_expr(_to_col(col))})")


def greatest(*cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"GREATEST({args})")


def hex(col: Column | str) -> Column:
    return Column(f"HEX({_to_expr(_to_col(col))})")


def hypot(col1: Column | str, col2: Column | str) -> Column:
    e1 = _to_expr(_to_col(col1))
    e2 = _to_expr(_to_col(col2))
    return Column(f"SQRT({e1}*{e1} + {e2}*{e2})")


def least(*cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"LEAST({args})")


def ln(col: Column | str) -> Column:
    return Column(f"LN({_to_expr(_to_col(col))})")


def log10(col: Column | str) -> Column:
    return Column(f"LOG10({_to_expr(_to_col(col))})")


def log1p(col: Column | str) -> Column:
    return Column(f"LOG(1 + {_to_expr(_to_col(col))})")


def log2(col: Column | str) -> Column:
    return Column(f"LOG2({_to_expr(_to_col(col))})")


def negate(col: Column | str) -> Column:
    return Column(f"-{_to_expr(_to_col(col))}")


def negative(col: Column | str) -> Column:
    return negate(col)


def pi() -> Column:
    return Column("PI()")


def pmod(col: Column | str, divisor: object) -> Column:
    return Column(f"({_to_expr(_to_col(col))} % {_to_expr(divisor)})")


def positive(col: Column | str) -> Column:
    return Column(f"+{_to_expr(_to_col(col))}")


def radians(col: Column | str) -> Column:
    return Column(f"RADIANS({_to_expr(_to_col(col))})")


def rand(seed: int | None = None) -> Column:
    if seed is not None:
        return Column(f"RAND({seed})")
    return Column("RAND()")


def randn(seed: int | None = None) -> Column:
    if seed is not None:
        return Column(f"RANDN({seed})")
    return Column("RANDN()")


def random(seed: int | None = None) -> Column:
    return rand(seed)


def rint(col: Column | str) -> Column:
    return Column(f"RINT({_to_expr(_to_col(col))})")


def sec(col: Column | str) -> Column:
    return Column(f"1 / COS({_to_expr(_to_col(col))})")


def sign(col: Column | str) -> Column:
    return Column(f"SIGN({_to_expr(_to_col(col))})")


def signum(col: Column | str) -> Column:
    return sign(col)


def sin(col: Column | str) -> Column:
    return Column(f"SIN({_to_expr(_to_col(col))})")


def sinh(col: Column | str) -> Column:
    return Column(f"SINH({_to_expr(_to_col(col))})")


def tan(col: Column | str) -> Column:
    return Column(f"TAN({_to_expr(_to_col(col))})")


def tanh(col: Column | str) -> Column:
    return Column(f"TANH({_to_expr(_to_col(col))})")


def try_add(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} + {_to_expr(_to_col(col2))}")


def try_divide(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} / {_to_expr(_to_col(col2))}")


def try_mod(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} % {_to_expr(_to_col(col2))}")


def try_multiply(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} * {_to_expr(_to_col(col2))}")


def try_subtract(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"{_to_expr(_to_col(col1))} - {_to_expr(_to_col(col2))}")


def unhex(col: Column | str) -> Column:
    return Column(f"UNHEX({_to_expr(_to_col(col))})")


def uniform(low: int | float, high: int | float, seed: int | None = None) -> Column:
    if seed is not None:
        return Column(f"UNIFORM({low}, {high}, {seed})")
    return Column(f"UNIFORM({low}, {high})")


def width_bucket(
    col: Column | str, min_value: object, max_value: object, nBuckets: object
) -> Column:  # noqa: E501
    return Column(
        f"WIDTH_BUCKET({_to_expr(_to_col(col))}, {_to_expr(min_value)}, {_to_expr(max_value)}, {_to_expr(nBuckets)})"  # noqa: E501
    )  # noqa: E501


# ── String functions ────────────────────────────────────────────────────


def ascii(col: Column | str) -> Column:
    return Column(f"ASCII({_to_expr(_to_col(col))})")


def base64(col: Column | str) -> Column:
    return Column(f"BASE64({_to_expr(_to_col(col))})")


def bit_length(col: Column | str) -> Column:
    return Column(f"BIT_LENGTH({_to_expr(_to_col(col))})")


def btrim(col: Column | str, trimStr: str | None = None) -> Column:
    if trimStr is not None:
        return Column(f"BTRIM({_to_expr(_to_col(col))}, '{trimStr}')")
    return Column(f"BTRIM({_to_expr(_to_col(col))})")


def char(col: Column | str) -> Column:
    return Column(f"CHAR({_to_expr(_to_col(col))})")


def char_length(col: Column | str) -> Column:
    return Column(f"CHAR_LENGTH({_to_expr(_to_col(col))})")


def character_length(col: Column | str) -> Column:
    return Column(f"CHARACTER_LENGTH({_to_expr(_to_col(col))})")


def chr(col: Column | str) -> Column:
    return Column(f"CHR({_to_expr(_to_col(col))})")


def collate(col: Column | str, collation_name: str) -> Column:
    return Column(f"{_to_expr(_to_col(col))} COLLATE {collation_name}")


def collation(col: Column | str) -> Column:
    return Column(f"COLLATION({_to_expr(_to_col(col))})")


def contains(col: Column | str, other: object) -> Column:
    return Column(f"CONTAINS({_to_expr(_to_col(col))}, {_to_expr(other)})")


def decode(col: Column | str, charset: str) -> Column:
    return Column(f"DECODE({_to_expr(_to_col(col))}, '{charset}')")


def elt(n: int, *strings: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(s)) for s in strings)
    return Column(f"ELT({n}, {args})")


def encode(col: Column | str, charset: str) -> Column:
    return Column(f"ENCODE({_to_expr(_to_col(col))}, '{charset}')")


def endswith(col: Column | str, suffix: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))} LIKE '%' || {_to_expr(suffix)}")


def find_in_set(str_val: Column | str, str_array: Column | str) -> Column:
    return Column(
        f"FIND_IN_SET({_to_expr(_to_col(str_val))}, {_to_expr(_to_col(str_array))})"
    )  # noqa: E501


def format_string(format_str: str, *args: object) -> Column:
    args_str = ", ".join(_to_expr(a) for a in args)
    return Column(f"FORMAT_STRING('{format_str}', {args_str})")


def instr(col: Column | str, substr: str) -> Column:
    return Column(f"INSTR({_to_expr(_to_col(col))}, '{substr}')")


def is_valid_utf8(col: Column | str) -> Column:
    return Column(f"IS_VALID_UTF8({_to_expr(_to_col(col))})")


def lcase(col: Column | str) -> Column:
    return lower(col)


def left(col: Column | str, length: int) -> Column:
    return Column(f"LEFT({_to_expr(_to_col(col))}, {length})")


def levenshtein(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"LEVENSHTEIN({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def locate(substr: str, col: Column | str, pos: int = 0) -> Column:
    if pos > 0:
        return Column(f"LOCATE('{substr}', {_to_expr(_to_col(col))}, {pos})")
    return Column(f"LOCATE('{substr}', {_to_expr(_to_col(col))})")


def lpad(col: Column | str, length: int, pad: str) -> Column:
    return Column(f"LPAD({_to_expr(_to_col(col))}, {length}, '{pad}')")


def make_valid_utf8(col: Column | str) -> Column:
    return Column(f"MAKE_VALID_UTF8({_to_expr(_to_col(col))})")


def mask(
    col: Column | str,
    upperChar: str = "X",
    lowerChar: str = "x",
    digitChar: str = "n",
    otherChar: str | None = None,
) -> Column:  # noqa: E501
    raise NotImplementedError("mask is not supported in SQL mode")


def octet_length(col: Column | str) -> Column:
    return Column(f"OCTET_LENGTH({_to_expr(_to_col(col))})")


def overlay(
    col: Column | str, replace: str, pos: int, length: int | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(col))
    if length is not None:
        return Column(f"OVERLAY({expr} PLACING '{replace}' FROM {pos} FOR {length})")
    return Column(f"OVERLAY({expr} PLACING '{replace}' FROM {pos})")


def position(substr: str, col: Column | str) -> Column:
    return Column(f"POSITION('{substr}' IN {_to_expr(_to_col(col))})")


def printf(format_str: str, *args: object) -> Column:
    args_str = ", ".join(_to_expr(a) for a in args)
    return Column(f"PRINTF('{format_str}', {args_str})")


def quote(col: Column | str) -> Column:
    return Column(f"QUOTE({_to_expr(_to_col(col))})")


def randstr(length: int, seed: int | None = None) -> Column:
    if seed is not None:
        return Column(f"RANDSTR({length}, {seed})")
    return Column(f"RANDSTR({length})")


def regexp_count(col: Column | str, regex: str) -> Column:
    return Column(f"REGEXP_COUNT({_to_expr(_to_col(col))}, '{regex}')")


def regexp_extract(col: Column | str, regex: str, idx: int = 1) -> Column:
    return Column(f"REGEXP_EXTRACT({_to_expr(_to_col(col))}, '{regex}', {idx})")


def regexp_extract_all(col: Column | str, regex: str, idx: int = 1) -> Column:
    return Column(f"REGEXP_EXTRACT_ALL({_to_expr(_to_col(col))}, '{regex}', {idx})")


def regexp_instr(col: Column | str, regex: str) -> Column:
    return Column(f"REGEXP_INSTR({_to_expr(_to_col(col))}, '{regex}')")


def regexp_replace(col: Column | str, regex: str, repl: str, pos: int = 1) -> Column:
    return Column(
        f"REGEXP_REPLACE({_to_expr(_to_col(col))}, '{regex}', '{repl}', {pos})"
    )  # noqa: E501


def regexp_substr(col: Column | str, regex: str) -> Column:
    return Column(f"REGEXP_SUBSTR({_to_expr(_to_col(col))}, '{regex}')")


def repeat(col: Column | str, n: int) -> Column:
    return Column(f"REPEAT({_to_expr(_to_col(col))}, {n})")


def right(col: Column | str, length: int) -> Column:
    return Column(f"RIGHT({_to_expr(_to_col(col))}, {length})")


def rpad(col: Column | str, length: int, pad: str) -> Column:
    return Column(f"RPAD({_to_expr(_to_col(col))}, {length}, '{pad}')")


def sentences(
    col: Column | str, lang: str | None = None, country: str | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(col))
    if lang is not None and country is not None:
        return Column(f"SENTENCES({expr}, '{lang}', '{country}')")
    if lang is not None:
        return Column(f"SENTENCES({expr}, '{lang}')")
    return Column(f"SENTENCES({expr})")


def soundex(col: Column | str) -> Column:
    return Column(f"SOUNDEX({_to_expr(_to_col(col))})")


def split_part(col: Column | str, delimiter: str, partNum: int) -> Column:
    return Column(f"SPLIT_PART({_to_expr(_to_col(col))}, '{delimiter}', {partNum})")


def startswith(col: Column | str, prefix: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))} LIKE {_to_expr(prefix)} || '%'")


def substr(col: Column | str, pos: int, length: int | None = None) -> Column:
    return substring(col, pos, length)


def substring_index(col: Column | str, delim: str, count: int) -> Column:
    return Column(f"SUBSTRING_INDEX({_to_expr(_to_col(col))}, '{delim}', {count})")


def to_binary(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_BINARY({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_BINARY({_to_expr(_to_col(col))})")


def to_char(col: Column | str, fmt: str) -> Column:
    return Column(f"TO_CHAR({_to_expr(_to_col(col))}, '{fmt}')")


def to_number(col: Column | str, fmt: str) -> Column:
    return Column(f"TO_NUMBER({_to_expr(_to_col(col))}, '{fmt}')")


def to_varchar(col: Column | str, fmt: str) -> Column:
    return Column(f"TO_VARCHAR({_to_expr(_to_col(col))}, '{fmt}')")


def translate(col: Column | str, from_str: str, to_str: str) -> Column:
    return Column(f"TRANSLATE({_to_expr(_to_col(col))}, '{from_str}', '{to_str}')")


def try_to_binary(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TRY_TO_BINARY({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TRY_TO_BINARY({_to_expr(_to_col(col))})")


def try_to_number(col: Column | str, fmt: str) -> Column:
    return Column(f"TRY_TO_NUMBER({_to_expr(_to_col(col))}, '{fmt}')")


def try_validate_utf8(col: Column | str) -> Column:
    return Column(f"TRY_VALIDATE_UTF8({_to_expr(_to_col(col))})")


def ucase(col: Column | str) -> Column:
    return upper(col)


def unbase64(col: Column | str) -> Column:
    return Column(f"UNBASE64({_to_expr(_to_col(col))})")


def validate_utf8(col: Column | str) -> Column:
    return Column(f"VALIDATE_UTF8({_to_expr(_to_col(col))})")


# ── Date / Time functions ───────────────────────────────────────────────


def add_months(col: Column | str, n: int) -> Column:
    return Column(f"ADD_MONTHS({_to_expr(_to_col(col))}, {n})")


def convert_timezone(fromTz: str, toTz: str, col: Column | str) -> Column:
    return Column(f"CONVERT_TIMEZONE('{fromTz}', '{toTz}', {_to_expr(_to_col(col))})")


def curdate() -> Column:
    return Column("CURRENT_DATE")


def current_time() -> Column:
    return Column("CURRENT_TIME")


def current_timezone() -> Column:
    return Column("CURRENT_TIMEZONE()")


def date_diff(end: Column | str, start: Column | str) -> Column:
    return Column(f"DATEDIFF({_to_expr(_to_col(end))}, {_to_expr(_to_col(start))})")


def date_format(col: Column | str, fmt: str) -> Column:
    return Column(f"DATE_FORMAT({_to_expr(_to_col(col))}, '{fmt}')")


def date_from_unix_date(col: Column | str) -> Column:
    return Column(f"DATE_FROM_UNIX_DATE({_to_expr(_to_col(col))})")


def date_part(field: str, col: Column | str) -> Column:
    return Column(f"DATE_PART('{field}', {_to_expr(_to_col(col))})")


def date_trunc(fmt: str, col: Column | str) -> Column:
    return Column(f"DATE_TRUNC('{fmt}', {_to_expr(_to_col(col))})")


def dateadd(col: Column | str, days: int) -> Column:
    return Column(f"DATE_ADD({_to_expr(_to_col(col))}, {days})")


def datepart(field: str, col: Column | str) -> Column:
    return Column(f"DATE_PART('{field}', {_to_expr(_to_col(col))})")


def dayname(col: Column | str) -> Column:
    return Column(f"DAYNAME({_to_expr(_to_col(col))})")


def dayofmonth(col: Column | str) -> Column:
    return Column(f"DAYOFMONTH({_to_expr(_to_col(col))})")


def dayofweek(col: Column | str) -> Column:
    return Column(f"DAYOFWEEK({_to_expr(_to_col(col))})")


def dayofyear(col: Column | str) -> Column:
    return Column(f"DAYOFYEAR({_to_expr(_to_col(col))})")


def extract(field: str, col: Column | str) -> Column:
    return Column(f"EXTRACT({field.upper()} FROM {_to_expr(_to_col(col))})")


def from_utc_timestamp(col: Column | str, tz: str) -> Column:
    return Column(f"FROM_UTC_TIMESTAMP({_to_expr(_to_col(col))}, '{tz}')")


def last_day(col: Column | str) -> Column:
    return Column(f"LAST_DAY({_to_expr(_to_col(col))})")


def localtimestamp() -> Column:
    return Column("LOCALTIMESTAMP")


def make_date(
    y: Column | int | str, m: Column | int | str, d: Column | int | str
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    return Column(f"MAKE_DATE({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)})")


def make_dt_interval(
    days: int = 0, hours: int = 0, mins: int = 0, secs: int = 0
) -> Column:  # noqa: E501
    return Column(f"MAKE_DT_INTERVAL({days}, {hours}, {mins}, {secs})")


def make_interval(
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    mins: int = 0,
    secs: int = 0,
) -> Column:  # noqa: E501
    return Column(
        f"MAKE_INTERVAL({years}, {months}, {weeks}, {days}, {hours}, {mins}, {secs})"
    )  # noqa: E501


def make_time(
    h: Column | int | str, m: Column | int | str, s: Column | int | str
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    return Column(f"MAKE_TIME({_to_col_lit(h)}, {_to_col_lit(m)}, {_to_col_lit(s)})")


def make_timestamp(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
    tz: str | None = None,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    if tz is not None:
        return Column(
            f"MAKE_TIMESTAMP({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)}, '{tz}')"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"MAKE_TIMESTAMP({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def make_timestamp_ltz(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
    tz: str | None = None,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    if tz is not None:
        return Column(
            f"MAKE_TIMESTAMP_LTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)}, '{tz}')"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"MAKE_TIMESTAMP_LTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def make_timestamp_ntz(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    return Column(
        f"MAKE_TIMESTAMP_NTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def make_ym_interval(years: int = 0, months: int = 0) -> Column:
    return Column(f"MAKE_YM_INTERVAL({years}, {months})")


def monthname(col: Column | str) -> Column:
    return Column(f"MONTHNAME({_to_expr(_to_col(col))})")


def months_between(
    col1: Column | str, col2: Column | str, roundOff: bool | None = None
) -> Column:  # noqa: E501
    args = f"{_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))}"
    if roundOff is not None:
        args = f"{args}, {_to_expr(roundOff)}"
    return Column(f"MONTHS_BETWEEN({args})")


def next_day(col: Column | str, dayOfWeek: str) -> Column:
    return Column(f"NEXT_DAY({_to_expr(_to_col(col))}, '{dayOfWeek}')")


def now() -> Column:
    return Column("NOW()")


def quarter(col: Column | str) -> Column:
    return Column(f"QUARTER({_to_expr(_to_col(col))})")


def session_window(col: Column | str, gapDuration: str) -> Column:
    raise NotImplementedError("session_window is not supported in SQL mode")


def timestamp_add(col: Column | str, n: int) -> Column:
    return Column(f"{_to_expr(_to_col(col))} + INTERVAL {n} DAYS")


def timestamp_diff(unit: str, start: Column | str, end: Column | str) -> Column:
    return Column(
        f"TIMESTAMPDIFF({unit}, {_to_expr(_to_col(start))}, {_to_expr(_to_col(end))})"
    )  # noqa: E501


def timestamp_micros(col: Column | str) -> Column:
    return Column(f"TIMESTAMP_MICROS({_to_expr(_to_col(col))})")


def timestamp_millis(col: Column | str) -> Column:
    return Column(f"TIMESTAMP_MILLIS({_to_expr(_to_col(col))})")


def timestamp_seconds(col: Column | str) -> Column:
    return Column(f"TIMESTAMP_SECONDS({_to_expr(_to_col(col))})")


def time_diff(unit: str, start: Column | str, end: Column | str) -> Column:
    return Column(
        f"TIME_DIFF({unit}, {_to_expr(_to_col(start))}, {_to_expr(_to_col(end))})"
    )  # noqa: E501


def time_trunc(fmt: str, col: Column | str) -> Column:
    return Column(f"TIME_TRUNC('{fmt}', {_to_expr(_to_col(col))})")


def to_date(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_DATE({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_DATE({_to_expr(_to_col(col))})")


def to_time(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_TIME({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_TIME({_to_expr(_to_col(col))})")


def to_timestamp(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_TIMESTAMP({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_TIMESTAMP({_to_expr(_to_col(col))})")


def to_timestamp_ltz(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_TIMESTAMP_LTZ({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_TIMESTAMP_LTZ({_to_expr(_to_col(col))})")


def to_timestamp_ntz(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_TIMESTAMP_NTZ({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_TIMESTAMP_NTZ({_to_expr(_to_col(col))})")


def to_unix_timestamp(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TO_UNIX_TIMESTAMP({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TO_UNIX_TIMESTAMP({_to_expr(_to_col(col))})")


def to_utc_timestamp(col: Column | str, tz: str) -> Column:
    return Column(f"TO_UTC_TIMESTAMP({_to_expr(_to_col(col))}, '{tz}')")


def trunc(col: Column | str, fmt: str) -> Column:
    return Column(f"TRUNC({_to_expr(_to_col(col))}, '{fmt}')")


def try_make_interval(
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    mins: int = 0,
    secs: int = 0,
) -> Column:  # noqa: E501
    return Column(
        f"TRY_MAKE_INTERVAL({years}, {months}, {weeks}, {days}, {hours}, {mins}, {secs})"  # noqa: E501
    )  # noqa: E501


def try_make_timestamp(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
    tz: str | None = None,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    if tz is not None:
        return Column(
            f"TRY_MAKE_TIMESTAMP({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)}, '{tz}')"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"TRY_MAKE_TIMESTAMP({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def try_make_timestamp_ltz(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
    tz: str | None = None,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    if tz is not None:
        return Column(
            f"TRY_MAKE_TIMESTAMP_LTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)}, '{tz}')"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"TRY_MAKE_TIMESTAMP_LTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def try_make_timestamp_ntz(
    y: Column | int | str,
    m: Column | int | str,
    d: Column | int | str,
    h: Column | int | str,
    mi: Column | int | str,
    s: Column | int | str,
) -> Column:  # noqa: E501
    def _to_col_lit(v: Column | int | str) -> str:
        if isinstance(v, str):
            return _to_expr(_to_col(v))
        return _to_expr(v)

    return Column(
        f"TRY_MAKE_TIMESTAMP_NTZ({_to_col_lit(y)}, {_to_col_lit(m)}, {_to_col_lit(d)}, {_to_col_lit(h)}, {_to_col_lit(mi)}, {_to_col_lit(s)})"  # noqa: E501
    )  # noqa: E501


def try_to_time(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TRY_TO_TIME({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TRY_TO_TIME({_to_expr(_to_col(col))})")


def try_to_timestamp(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TRY_TO_TIMESTAMP({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TRY_TO_TIMESTAMP({_to_expr(_to_col(col))})")


def try_to_date(col: Column | str, fmt: str | None = None) -> Column:
    if fmt is not None:
        return Column(f"TRY_TO_DATE({_to_expr(_to_col(col))}, '{fmt}')")
    return Column(f"TRY_TO_DATE({_to_expr(_to_col(col))})")


def unix_date(col: Column | str) -> Column:
    return Column(f"UNIX_DATE({_to_expr(_to_col(col))})")


def unix_micros(col: Column | str) -> Column:
    return Column(f"UNIX_MICROS({_to_expr(_to_col(col))})")


def unix_millis(col: Column | str) -> Column:
    return Column(f"UNIX_MILLIS({_to_expr(_to_col(col))})")


def unix_seconds(col: Column | str) -> Column:
    return Column(f"UNIX_SECONDS({_to_expr(_to_col(col))})")


def weekday(col: Column | str) -> Column:
    return Column(f"WEEKDAY({_to_expr(_to_col(col))})")


def weekofyear(col: Column | str) -> Column:
    return Column(f"WEEKOFYEAR({_to_expr(_to_col(col))})")


def window(col: Column | str, windowDuration: str) -> Column:
    return Column(f"WINDOW({_to_expr(_to_col(col))}, '{windowDuration}')")


def window_time(col: Column | str) -> Column:
    return Column(f"WINDOW_TIME({_to_expr(_to_col(col))})")


# ── Bitwise functions ───────────────────────────────────────────────────


def bit_count(col: Column | str) -> Column:
    return Column(f"BIT_COUNT({_to_expr(_to_col(col))})")


def bit_get(col: Column | str, pos: object) -> Column:
    return Column(f"BIT_GET({_to_expr(_to_col(col))}, {_to_expr(pos)})")


def bitwise_not(col: Column | str) -> Column:
    return Column(f"~({_to_expr(_to_col(col))})")


def getbit(col: Column | str, pos: object) -> Column:
    return Column(f"GETBIT({_to_expr(_to_col(col))}, {_to_expr(pos)})")


def shiftleft(col: Column | str, n: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))} << {_to_expr(n)}")


def shiftright(col: Column | str, n: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))} >> {_to_expr(n)}")


def shiftrightunsigned(col: Column | str, n: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))} >> {_to_expr(n)}")


# ── Hash functions ──────────────────────────────────────────────────────


def crc32(col: Column | str) -> Column:
    return Column(f"CRC32({_to_expr(_to_col(col))})")


def hash(*cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"HASH({args})")


def md5(col: Column | str) -> Column:
    return Column(f"MD5({_to_expr(_to_col(col))})")


def sha(col: Column | str) -> Column:
    return Column(f"SHA({_to_expr(_to_col(col))})")


def sha1(col: Column | str) -> Column:
    return Column(f"SHA1({_to_expr(_to_col(col))})")


def sha2(col: Column | str, bit_length: object) -> Column:
    return Column(f"SHA2({_to_expr(_to_col(col))}, {_to_expr(bit_length)})")


def xxhash64(*cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"XXHASH64({args})")


# ── Aggregate functions ─────────────────────────────────────────────────


def any_value(column: Column | str) -> Column:
    return Column(f"ANY_VALUE({_to_expr(_to_col(column))})")


def approx_count_distinct(column: Column | str, rsd: float | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if rsd is not None:
        return Column(f"APPROX_COUNT_DISTINCT({expr}, {rsd})")
    return Column(f"APPROX_COUNT_DISTINCT({expr})")


def approx_percentile(
    column: Column | str, percentage: object, accuracy: int | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(column))
    if accuracy is not None:
        return Column(f"APPROX_PERCENTILE({expr}, {_to_expr(percentage)}, {accuracy})")
    return Column(f"APPROX_PERCENTILE({expr}, {_to_expr(percentage)})")


def array_agg(column: Column | str) -> Column:
    return Column(f"ARRAY_AGG({_to_expr(_to_col(column))})")


def bit_and(column: Column | str) -> Column:
    return Column(f"BIT_AND({_to_expr(_to_col(column))})")


def bit_or(column: Column | str) -> Column:
    return Column(f"BIT_OR({_to_expr(_to_col(column))})")


def bit_xor(column: Column | str) -> Column:
    return Column(f"BIT_XOR({_to_expr(_to_col(column))})")


def bitmap_construct_agg(column: Column | str) -> Column:
    return Column(f"BITMAP_CONSTRUCT_AGG({_to_expr(_to_col(column))})")


def bitmap_or_agg(column: Column | str) -> Column:
    return Column(f"BITMAP_OR_AGG({_to_expr(_to_col(column))})")


def bool_and(column: Column | str) -> Column:
    return Column(f"BOOL_AND({_to_expr(_to_col(column))})")


def bool_or(column: Column | str) -> Column:
    return Column(f"BOOL_OR({_to_expr(_to_col(column))})")


def collect_list(column: Column | str) -> Column:
    return Column(f"COLLECT_LIST({_to_expr(_to_col(column))})")


def collect_set(column: Column | str) -> Column:
    return Column(f"COLLECT_SET({_to_expr(_to_col(column))})")


def corr(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"CORR({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def count_distinct(*columns: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in columns)
    return Column(f"COUNT(DISTINCT {args})")


def count_if(column: Column | str) -> Column:
    return Column(f"COUNT_IF({_to_expr(_to_col(column))})")


def count_min_sketch(
    column: Column | str, eps: object, conf: object, seed: object
) -> Column:  # noqa: E501
    raise NotImplementedError("count_min_sketch is not supported in SQL mode")


def covar_pop(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"COVAR_POP({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def covar_samp(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"COVAR_SAMP({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def every(column: Column | str) -> Column:
    return Column(f"BOOL_AND({_to_expr(_to_col(column))})")


def first(column: Column | str, ignorenulls: bool | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if ignorenulls is not None:
        return Column(f"FIRST({expr}, {_to_expr(ignorenulls)})")
    return Column(f"FIRST({expr})")


def first_value(column: Column | str, ignorenulls: bool | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if ignorenulls is not None:
        return Column(f"FIRST_VALUE({expr}, {_to_expr(ignorenulls)})")
    return Column(f"FIRST_VALUE({expr})")


def grouping(column: Column | str) -> Column:
    return Column(f"GROUPING({_to_expr(_to_col(column))})")


def grouping_id(*columns: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in columns)
    return Column(f"GROUPING_ID({args})")


def histogram_numeric(column: Column | str, n_bins: int) -> Column:
    return Column(f"HISTOGRAM_NUMERIC({_to_expr(_to_col(column))}, {n_bins})")


def hll_sketch_agg(column: Column | str, lg_config_k: int | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if lg_config_k is not None:
        return Column(f"HLL_SKETCH_AGG({expr}, {lg_config_k})")
    return Column(f"HLL_SKETCH_AGG({expr})")


def hll_union_agg(
    column: Column | str, allow_different_lg_config_k: bool | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(column))
    if allow_different_lg_config_k is not None:
        return Column(f"HLL_UNION_AGG({expr}, {_to_expr(allow_different_lg_config_k)})")
    return Column(f"HLL_UNION_AGG({expr})")


def kurtosis(column: Column | str) -> Column:
    return Column(f"KURTOSIS({_to_expr(_to_col(column))})")


def last(column: Column | str, ignorenulls: bool | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if ignorenulls is not None:
        return Column(f"LAST({expr}, {_to_expr(ignorenulls)})")
    return Column(f"LAST({expr})")


def last_value(column: Column | str, ignorenulls: bool | None = None) -> Column:
    expr = _to_expr(_to_col(column))
    if ignorenulls is not None:
        return Column(f"LAST_VALUE({expr}, {_to_expr(ignorenulls)})")
    return Column(f"LAST_VALUE({expr})")


def listagg(column: Column | str, sep: str) -> Column:
    return Column(f"LISTAGG({_to_expr(_to_col(column))}, {_to_expr(sep)})")


def listagg_distinct(column: Column | str, sep: str) -> Column:
    return Column(f"LISTAGG(DISTINCT {_to_expr(_to_col(column))}, {_to_expr(sep)})")


def max_by(column: Column | str, ord: Column | str) -> Column:
    return Column(f"MAX_BY({_to_expr(_to_col(column))}, {_to_expr(_to_col(ord))})")


def mean(column: Column | str) -> Column:
    return Column(f"AVG({_to_expr(_to_col(column))})")


def median(column: Column | str) -> Column:
    return Column(f"MEDIAN({_to_expr(_to_col(column))})")


def min_by(column: Column | str, ord: Column | str) -> Column:
    return Column(f"MIN_BY({_to_expr(_to_col(column))}, {_to_expr(_to_col(ord))})")


def mode(column: Column | str) -> Column:
    return Column(f"MODE({_to_expr(_to_col(column))})")


def percentile(
    column: Column | str, percentage: object, frequency: Column | str | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(column))
    pct = _to_expr(percentage)
    if frequency is not None:
        return Column(f"PERCENTILE({expr}, {pct}, {_to_expr(_to_col(frequency))})")
    return Column(f"PERCENTILE({expr}, {pct})")


def percentile_approx(
    column: Column | str, percentage: object, accuracy: int | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(column))
    pct = _to_expr(percentage)
    if accuracy is not None:
        return Column(f"PERCENTILE_APPROX({expr}, {pct}, {accuracy})")
    return Column(f"PERCENTILE_APPROX({expr}, {pct})")


def product(column: Column | str) -> Column:
    return Column(f"PRODUCT({_to_expr(_to_col(column))})")


def regr_avgx(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_AVGX({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_avgy(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_AVGY({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_count(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_COUNT({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_intercept(col1: Column | str, col2: Column | str) -> Column:
    return Column(
        f"REGR_INTERCEPT({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})"
    )  # noqa: E501


def regr_r2(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_R2({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_slope(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_SLOPE({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_sxx(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_SXX({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_sxy(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_SXY({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def regr_syy(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"REGR_SYY({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def skewness(column: Column | str) -> Column:
    return Column(f"SKEWNESS({_to_expr(_to_col(column))})")


def some(column: Column | str) -> Column:
    return Column(f"BOOL_OR({_to_expr(_to_col(column))})")


def std(column: Column | str) -> Column:
    return Column(f"STD({_to_expr(_to_col(column))})")


def stddev(column: Column | str) -> Column:
    return Column(f"STDDEV({_to_expr(_to_col(column))})")


def stddev_pop(column: Column | str) -> Column:
    return Column(f"STDDEV_POP({_to_expr(_to_col(column))})")


def stddev_samp(column: Column | str) -> Column:
    return Column(f"STDDEV_SAMP({_to_expr(_to_col(column))})")


def string_agg(column: Column | str, sep: str) -> Column:
    return Column(f"STRING_AGG({_to_expr(_to_col(column))}, {_to_expr(sep)})")


def string_agg_distinct(column: Column | str, sep: str) -> Column:
    return Column(f"STRING_AGG(DISTINCT {_to_expr(_to_col(column))}, {_to_expr(sep)})")


def sum_distinct(column: Column | str) -> Column:
    return Column(f"SUM(DISTINCT {_to_expr(_to_col(column))})")


def try_avg(column: Column | str) -> Column:
    return Column(f"TRY_AVG({_to_expr(_to_col(column))})")


def try_sum(column: Column | str) -> Column:
    return Column(f"TRY_SUM({_to_expr(_to_col(column))})")


def var_pop(column: Column | str) -> Column:
    return Column(f"VAR_POP({_to_expr(_to_col(column))})")


def var_samp(column: Column | str) -> Column:
    return Column(f"VAR_SAMP({_to_expr(_to_col(column))})")


def variance(column: Column | str) -> Column:
    return Column(f"VAR_SAMP({_to_expr(_to_col(column))})")


# ── Window / Analytic functions ─────────────────────────────────────────


def cume_dist() -> Column:
    return Column("CUME_DIST()")


def nth_value(col: Column | str, offset: int) -> Column:
    return Column(f"NTH_VALUE({_to_expr(_to_col(col))}, {offset})")


def ntile(n: int) -> Column:
    return Column(f"NTILE({n})")


def percent_rank() -> Column:
    return Column("PERCENT_RANK()")


# ── Generator / Explode functions ───────────────────────────────────────


def explode(col: Column | str) -> Column:
    return Column(f"EXPLODE({_to_expr(_to_col(col))})")


def explode_outer(col: Column | str) -> Column:
    return Column(f"EXPLODE_OUTER({_to_expr(_to_col(col))})")


def inline(col: Column | str) -> Column:
    return Column(f"INLINE({_to_expr(_to_col(col))})")


def inline_outer(col: Column | str) -> Column:
    return Column(f"INLINE_OUTER({_to_expr(_to_col(col))})")


def posexplode(col: Column | str) -> Column:
    return Column(f"POSEXPLODE({_to_expr(_to_col(col))})")


def posexplode_outer(col: Column | str) -> Column:
    return Column(f"POSEXPLODE_OUTER({_to_expr(_to_col(col))})")


def stack(n: int, *cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"STACK({n}, {args})")


# ── Map / Struct functions ──────────────────────────────────────────────


def named_struct(*name_val_pairs: object) -> Column:
    args = ", ".join(_to_expr(v) for v in name_val_pairs)
    return Column(f"NAMED_STRUCT({args})")


def struct(*cols: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(c)) for c in cols)
    return Column(f"STRUCT({args})")


def create_map(*keys_vals: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(v)) for v in keys_vals)
    return Column(f"MAP({args})")


def map_concat(*maps: Column | str) -> Column:
    args = ", ".join(_to_expr(_to_col(m)) for m in maps)
    return Column(f"MAP_CONCAT({args})")


def map_contains_key(map_col: Column | str, key: object) -> Column:
    return Column(f"MAP_CONTAINS_KEY({_to_expr(_to_col(map_col))}, {_to_expr(key)})")


def map_entries(map_col: Column | str) -> Column:
    return Column(f"MAP_ENTRIES({_to_expr(_to_col(map_col))})")


def map_from_arrays(keys: Column | str, vals: Column | str) -> Column:
    return Column(
        f"MAP_FROM_ARRAYS({_to_expr(_to_col(keys))}, {_to_expr(_to_col(vals))})"
    )  # noqa: E501


def map_from_entries(entries: Column | str) -> Column:
    return Column(f"MAP_FROM_ENTRIES({_to_expr(_to_col(entries))})")


def map_keys(map_col: Column | str) -> Column:
    return Column(f"MAP_KEYS({_to_expr(_to_col(map_col))})")


def map_values(map_col: Column | str) -> Column:
    return Column(f"MAP_VALUES({_to_expr(_to_col(map_col))})")


def str_to_map(
    str_col: Column | str, delim: str | None = None, pair_delim: str | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(str_col))
    if delim is not None and pair_delim is not None:
        return Column(f"STR_TO_MAP({expr}, {_to_expr(delim)}, {_to_expr(pair_delim)})")
    if delim is not None:
        return Column(f"STR_TO_MAP({expr}, {_to_expr(delim)})")
    if pair_delim is not None:
        return Column(f"STR_TO_MAP({expr}, {_to_expr(pair_delim)})")
    return Column(f"STR_TO_MAP({expr})")


# ── Array functions ─────────────────────────────────────────────────────


def array(*cols: Column | str) -> Column:
    return Column(f"ARRAY({', '.join(_to_expr(_to_col(c)) for c in cols)})")


def array_append(col: Column | str, val: object) -> Column:
    return Column(f"ARRAY_APPEND({_to_expr(_to_col(col))}, {_to_expr(val)})")


def array_compact(col: Column | str) -> Column:
    return Column(f"ARRAY_COMPACT({_to_expr(_to_col(col))})")


def array_contains(col: Column | str, val: object) -> Column:
    return Column(f"ARRAY_CONTAINS({_to_expr(_to_col(col))}, {_to_expr(val)})")


def array_distinct(col: Column | str) -> Column:
    return Column(f"ARRAY_DISTINCT({_to_expr(_to_col(col))})")


def array_except(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"ARRAY_EXCEPT({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def array_insert(col: Column | str, idx: object, val: object) -> Column:
    return Column(
        f"ARRAY_INSERT({_to_expr(_to_col(col))}, {_to_expr(idx)}, {_to_expr(val)})"
    )  # noqa: E501


def array_intersect(col1: Column | str, col2: Column | str) -> Column:
    return Column(
        f"ARRAY_INTERSECT({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})"
    )  # noqa: E501


def array_join(col: Column | str, sep: str, null_repl: str | None = None) -> Column:
    if null_repl is not None:
        return Column(f"ARRAY_JOIN({_to_expr(_to_col(col))}, '{sep}', '{null_repl}')")
    return Column(f"ARRAY_JOIN({_to_expr(_to_col(col))}, '{sep}')")


def array_max(col: Column | str) -> Column:
    return Column(f"ARRAY_MAX({_to_expr(_to_col(col))})")


def array_min(col: Column | str) -> Column:
    return Column(f"ARRAY_MIN({_to_expr(_to_col(col))})")


def array_position(col: Column | str, val: object) -> Column:
    return Column(f"ARRAY_POSITION({_to_expr(_to_col(col))}, {_to_expr(val)})")


def array_prepend(col: Column | str, val: object) -> Column:
    return Column(f"ARRAY_PREPEND({_to_expr(_to_col(col))}, {_to_expr(val)})")


def array_remove(col: Column | str, val: object) -> Column:
    return Column(f"ARRAY_REMOVE({_to_expr(_to_col(col))}, {_to_expr(val)})")


def array_repeat(col: Column | str, n: object) -> Column:
    return Column(f"ARRAY_REPEAT({_to_expr(_to_col(col))}, {_to_expr(n)})")


def array_size(col: Column | str) -> Column:
    return Column(f"ARRAY_SIZE({_to_expr(_to_col(col))})")


def array_sort(expr: Column | str, comparator: str | None = None) -> Column:
    if comparator is not None:
        return Column(f"ARRAY_SORT({_to_expr(_to_col(expr))}, {comparator})")
    return Column(f"ARRAY_SORT({_to_expr(_to_col(expr))})")


def array_union(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"ARRAY_UNION({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def arrays_overlap(col1: Column | str, col2: Column | str) -> Column:
    return Column(
        f"ARRAYS_OVERLAP({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})"
    )  # noqa: E501


def arrays_zip(*cols: Column | str) -> Column:
    return Column(f"ARRAYS_ZIP({', '.join(_to_expr(_to_col(c)) for c in cols)})")


def aggregate(
    expr: Column | str, init: Column | str, merge: str, finish: str | None = None
) -> Column:  # noqa: E501
    if finish is not None:
        return Column(
            f"AGGREGATE({_to_expr(_to_col(expr))}, {_to_expr(_to_col(init))}, {merge}, {finish})"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"AGGREGATE({_to_expr(_to_col(expr))}, {_to_expr(_to_col(init))}, {merge})"
    )  # noqa: E501


def cardinality(expr: Column | str) -> Column:
    return Column(f"CARDINALITY({_to_expr(_to_col(expr))})")


def element_at(col: Column | str, idx: object) -> Column:
    return Column(f"ELEMENT_AT({_to_expr(_to_col(col))}, {_to_expr(idx)})")


def exists(expr: Column | str, pred: str) -> Column:
    return Column(f"EXISTS({_to_expr(_to_col(expr))}, {pred})")


def filter(expr: Column | str, func: str) -> Column:
    return Column(f"FILTER({_to_expr(_to_col(expr))}, {func})")


def flatten(col: Column | str) -> Column:
    return Column(f"FLATTEN({_to_expr(_to_col(col))})")


def forall(expr: Column | str, pred: str) -> Column:
    return Column(f"FORALL({_to_expr(_to_col(expr))}, {pred})")


def get(col: Column | str, idx: object) -> Column:
    return Column(f"{_to_expr(_to_col(col))}[{_to_expr(idx)}]")


def map_filter(expr: Column | str, func: str) -> Column:
    return Column(f"MAP_FILTER({_to_expr(_to_col(expr))}, {func})")


def map_zip_with(map1: Column | str, map2: Column | str, func: str) -> Column:
    return Column(
        f"MAP_ZIP_WITH({_to_expr(_to_col(map1))}, {_to_expr(_to_col(map2))}, {func})"
    )  # noqa: E501


def reduce(
    expr: Column | str, init: Column | str, merge: str, finish: str | None = None
) -> Column:  # noqa: E501
    if finish is not None:
        return Column(
            f"REDUCE({_to_expr(_to_col(expr))}, {_to_expr(_to_col(init))}, {merge}, {finish})"  # noqa: E501
        )  # noqa: E501
    return Column(
        f"REDUCE({_to_expr(_to_col(expr))}, {_to_expr(_to_col(init))}, {merge})"
    )  # noqa: E501


def sequence(
    start: Column | str, stop: Column | str, step: Column | str | None = None
) -> Column:  # noqa: E501
    if step is not None:
        return Column(
            f"SEQUENCE({_to_expr(_to_col(start))}, {_to_expr(_to_col(stop))}, {_to_expr(_to_col(step))})"  # noqa: E501
        )  # noqa: E501
    return Column(f"SEQUENCE({_to_expr(_to_col(start))}, {_to_expr(_to_col(stop))})")


def shuffle(col: Column | str) -> Column:
    return Column(f"SHUFFLE({_to_expr(_to_col(col))})")


def size(col: Column | str) -> Column:
    return Column(f"SIZE({_to_expr(_to_col(col))})")


def slice(col: Column | str, start: object, len: object) -> Column:
    return Column(
        f"SLICE({_to_expr(_to_col(col))}, {_to_expr(start)}, {_to_expr(len)})"
    )  # noqa: E501


def sort_array(col: Column | str, asc: bool = True) -> Column:
    base = _to_expr(_to_col(col))
    if asc:
        return Column(f"SORT_ARRAY({base})")
    return Column(f"SORT_ARRAY({base}, FALSE)")


def transform(expr: Column | str, func: str) -> Column:
    return Column(f"TRANSFORM({_to_expr(_to_col(expr))}, {func})")


def transform_keys(expr: Column | str, func: str) -> Column:
    return Column(f"TRANSFORM_KEYS({_to_expr(_to_col(expr))}, {func})")


def transform_values(expr: Column | str, func: str) -> Column:
    return Column(f"TRANSFORM_VALUES({_to_expr(_to_col(expr))}, {func})")


def try_element_at(col: Column | str, idx: object) -> Column:
    return Column(f"TRY_ELEMENT_AT({_to_expr(_to_col(col))}, {_to_expr(idx)})")


def zip_with(left: Column | str, right: Column | str, func: str) -> Column:
    return Column(
        f"ZIP_WITH({_to_expr(_to_col(left))}, {_to_expr(_to_col(right))}, {func})"
    )  # noqa: E501


# ── CSV / JSON functions ────────────────────────────────────────────────


def from_csv(col: Column | str, schema: str, options: dict | None = None) -> Column:
    return Column(f"FROM_CSV({_to_expr(_to_col(col))}, {_to_expr(schema)})")


def schema_of_csv(csv: Column | str, options: dict | None = None) -> Column:
    return Column(f"SCHEMA_OF_CSV({_to_expr(_to_col(csv))})")


def to_csv(col: Column | str, options: dict | None = None) -> Column:
    return Column(f"TO_CSV({_to_expr(_to_col(col))})")


def from_json(col: Column | str, schema: str, options: dict | None = None) -> Column:
    return Column(f"FROM_JSON({_to_expr(_to_col(col))}, {_to_expr(schema)})")


def get_json_object(col: Column | str, path: str) -> Column:
    return Column(f"GET_JSON_OBJECT({_to_expr(_to_col(col))}, {_to_expr(path)})")


def json_array_length(col: Column | str, path: str | None = None) -> Column:
    expr = _to_expr(_to_col(col))
    if path is not None:
        return Column(f"JSON_ARRAY_LENGTH({expr}, {_to_expr(path)})")
    return Column(f"JSON_ARRAY_LENGTH({expr})")


def json_object_keys(col: Column | str, path: str | None = None) -> Column:
    expr = _to_expr(_to_col(col))
    if path is not None:
        return Column(f"JSON_OBJECT_KEYS({expr}, {_to_expr(path)})")
    return Column(f"JSON_OBJECT_KEYS({expr})")


def json_tuple(col: Column | str, *fields: str) -> Column:
    field_strs = ", ".join(_to_expr(f) for f in fields)
    return Column(f"JSON_TUPLE({_to_expr(_to_col(col))}, {field_strs})")


def schema_of_json(json: Column | str, options: dict | None = None) -> Column:
    return Column(f"SCHEMA_OF_JSON({_to_expr(_to_col(json))})")


def to_json(col: Column | str, options: dict | None = None) -> Column:
    return Column(f"TO_JSON({_to_expr(_to_col(col))})")


# ── URL functions ───────────────────────────────────────────────────────


def parse_url(
    url: Column | str, part_to_extract: str, key: str | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(url))
    if key is not None:
        return Column(
            f"PARSE_URL({expr}, {_to_expr(part_to_extract)}, {_to_expr(key)})"
        )  # noqa: E501
    return Column(f"PARSE_URL({expr}, {_to_expr(part_to_extract)})")


def try_parse_url(
    url: Column | str, part_to_extract: str, key: str | None = None
) -> Column:  # noqa: E501
    expr = _to_expr(_to_col(url))
    if key is not None:
        return Column(
            f"TRY_PARSE_URL({expr}, {_to_expr(part_to_extract)}, {_to_expr(key)})"
        )  # noqa: E501
    return Column(f"TRY_PARSE_URL({expr}, {_to_expr(part_to_extract)})")


def url_decode(str_col: Column | str) -> Column:
    return Column(f"URL_DECODE({_to_expr(_to_col(str_col))})")


def url_encode(str_col: Column | str) -> Column:
    return Column(f"URL_ENCODE({_to_expr(_to_col(str_col))})")


def try_url_decode(str_col: Column | str) -> Column:
    return Column(f"TRY_URL_DECODE({_to_expr(_to_col(str_col))})")


# ── Security / Misc functions ───────────────────────────────────────────


def aes_decrypt(col: Column | str, key: str, *args: object, **kwargs: object) -> Column:
    return Column(f"AES_DECRYPT({_to_expr(_to_col(col))}, {_to_expr(key)})")


def aes_encrypt(col: Column | str, key: str, *args: object, **kwargs: object) -> Column:
    return Column(f"AES_ENCRYPT({_to_expr(_to_col(col))}, {_to_expr(key)})")


def assert_true(col: Column | str, err_msg: str | None = None) -> Column:
    expr = _to_expr(_to_col(col))
    if err_msg is not None:
        return Column(f"ASSERT_TRUE({expr}, {_to_expr(err_msg)})")
    return Column(f"ASSERT_TRUE({expr})")


def bitmap_bit_position(col: Column | str) -> Column:
    return Column(f"BITMAP_BIT_POSITION({_to_expr(_to_col(col))})")


def bitmap_bucket_number(col: Column | str) -> Column:
    return Column(f"BITMAP_BUCKET_NUMBER({_to_expr(_to_col(col))})")


def bitmap_count(col: Column | str) -> Column:
    return Column(f"BITMAP_COUNT({_to_expr(_to_col(col))})")


def current_catalog() -> Column:
    return Column("CURRENT_CATALOG()")


def current_database() -> Column:
    return Column("CURRENT_DATABASE()")


def current_schema() -> Column:
    return Column("CURRENT_SCHEMA()")


def current_user() -> Column:
    return Column("CURRENT_USER()")


def hll_sketch_estimate(col: Column | str) -> Column:
    return Column(f"HLL_SKETCH_ESTIMATE({_to_expr(_to_col(col))})")


def hll_union(col1: Column | str, col2: Column | str) -> Column:
    return Column(f"HLL_UNION({_to_expr(_to_col(col1))}, {_to_expr(_to_col(col2))})")


def input_file_block_length() -> Column:
    return Column("INPUT_FILE_BLOCK_LENGTH()")


def input_file_block_start() -> Column:
    return Column("INPUT_FILE_BLOCK_START()")


def input_file_name() -> Column:
    return Column("INPUT_FILE_NAME()")


def java_method(cls: str, method: str, *args: object) -> Column:
    raise NotImplementedError("java_method is not supported in SQL mode")


def monotonically_increasing_id() -> Column:
    return Column("MONOTONICALLY_INCREASING_ID()")


def raise_error(col: Column | str) -> Column:
    return Column(f"RAISE_ERROR({_to_expr(_to_col(col))})")


def reflect(cls: str, method: str, *args: object) -> Column:
    raise NotImplementedError("reflect is not supported in SQL mode")


def session_user() -> Column:
    return Column("SESSION_USER()")


def spark_partition_id() -> Column:
    return Column("SPARK_PARTITION_ID()")


def typeof(col: Column | str) -> Column:
    return Column(f"TYPEOF({_to_expr(_to_col(col))})")


def user() -> Column:
    return Column("CURRENT_USER()")


def uuid() -> Column:
    return Column("UUID()")


def version() -> Column:
    return Column("VERSION()")


def try_aes_decrypt(
    col: Column | str, key: str, *args: object, **kwargs: object
) -> Column:  # noqa: E501
    return Column(f"TRY_AES_DECRYPT({_to_expr(_to_col(col))}, {_to_expr(key)})")


def try_reflect(cls: str, method: str, *args: object) -> Column:
    raise NotImplementedError("try_reflect is not supported in SQL mode")


# ── Spatial / ST functions ──────────────────────────────────────────────


def st_asbinary(col: Column | str) -> Column:
    return Column(f"ST_ASBINARY({_to_expr(_to_col(col))})")


def st_geogfromwkb(col: Column | str) -> Column:
    return Column(f"ST_GEOGFROMWKB({_to_expr(_to_col(col))})")


def st_geomfromwkb(col: Column | str) -> Column:
    return Column(f"ST_GEOMFROMWKB({_to_expr(_to_col(col))})")


def st_setsrid(col: Column | str, srid: int) -> Column:
    return Column(f"ST_SETSRID({_to_expr(_to_col(col))}, {srid})")


def st_srid(col: Column | str) -> Column:
    return Column(f"ST_SRID({_to_expr(_to_col(col))})")


# ── Variant functions ───────────────────────────────────────────────────


def is_variant_null(col: Column | str) -> Column:
    return Column(f"IS_VARIANT_NULL({_to_expr(_to_col(col))})")


def parse_json(col: Column | str) -> Column:
    return Column(f"PARSE_JSON({_to_expr(_to_col(col))})")


def schema_of_variant(col: Column | str) -> Column:
    return Column(f"SCHEMA_OF_VARIANT({_to_expr(_to_col(col))})")


def schema_of_variant_agg(col: Column | str) -> Column:
    return Column(f"SCHEMA_OF_VARIANT_AGG({_to_expr(_to_col(col))})")


def try_variant_get(col: Column | str, path: str, type_str: str) -> Column:
    return Column(
        f"TRY_VARIANT_GET({_to_expr(_to_col(col))}, {_to_expr(path)}, {_to_expr(type_str)})"  # noqa: E501
    )  # noqa: E501


def variant_get(col: Column | str, path: str, type_str: str) -> Column:
    return Column(
        f"VARIANT_GET({_to_expr(_to_col(col))}, {_to_expr(path)}, {_to_expr(type_str)})"
    )  # noqa: E501


def try_parse_json(col: Column | str) -> Column:
    return Column(f"TRY_PARSE_JSON({_to_expr(_to_col(col))})")


def to_variant_object(col: Column | str) -> Column:
    return Column(f"TO_VARIANT_OBJECT({_to_expr(_to_col(col))})")


# ── XML functions ───────────────────────────────────────────────────────


def from_xml(col: Column | str, schema: str, options: dict | None = None) -> Column:
    return Column(f"FROM_XML({_to_expr(_to_col(col))}, {_to_expr(schema)})")


def schema_of_xml(xml: Column | str, options: dict | None = None) -> Column:
    return Column(f"SCHEMA_OF_XML({_to_expr(_to_col(xml))})")


def to_xml(col: Column | str, options: dict | None = None) -> Column:
    return Column(f"TO_XML({_to_expr(_to_col(col))})")


def xpath(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_boolean(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_BOOLEAN({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_double(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_DOUBLE({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_float(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_FLOAT({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_int(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_INT({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_long(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_LONG({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_number(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_NUMBER({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_short(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_SHORT({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


def xpath_string(col: Column | str, xpath_str: str) -> Column:
    return Column(f"XPATH_STRING({_to_expr(_to_col(col))}, {_to_expr(xpath_str)})")


# ── UDF functions ───────────────────────────────────────────────────────


def udf(f: object, returnType: object = None) -> Column:
    raise NotImplementedError("udf is not supported in SQL mode")


def udtf(f: object, returnType: object = None) -> Column:
    raise NotImplementedError("udtf is not supported in SQL mode")


def pandas_udf(f: object, returnType: object = None) -> Column:
    raise NotImplementedError("pandas_udf is not supported in SQL mode")


def arrow_udf(f: object, returnType: object = None) -> Column:
    raise NotImplementedError("arrow_udf is not supported in SQL mode")


def arrow_udtf(f: object, returnType: object = None) -> Column:
    raise NotImplementedError("arrow_udtf is not supported in SQL mode")


def call_udf(name: str, *args: Column | str) -> Column:
    arg_strs = ", ".join(_to_expr(_to_col(a)) for a in args)
    return Column(f"{name}({arg_strs})")


def unwrap_udt(col: Column | str) -> Column:
    raise NotImplementedError("unwrap_udt is not supported in SQL mode")
