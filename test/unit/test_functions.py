from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.column import Column


def test_col() -> None:
    c = F.col("id")
    assert isinstance(c, Column)
    assert c._expr == "`id`"


def test_lit_string() -> None:
    c = F.lit("hello")
    assert c._expr == "'hello'"


def test_lit_int() -> None:
    c = F.lit(42)
    assert c._expr == "42"


def test_lit_null() -> None:
    c = F.lit(None)
    assert c._expr == "NULL"


def test_lit_bool() -> None:
    c = F.lit(True)
    assert c._expr == "TRUE"


def test_count_star() -> None:
    c = F.count()
    assert c._expr == "COUNT(*)"


def test_count_column() -> None:
    c = F.count(F.col("id"))
    assert c._expr == "COUNT(`id`)"


def test_count_distinct() -> None:
    c = F.countDistinct(F.col("category"))
    assert c._expr == "COUNT(DISTINCT `category`)"


def test_sum() -> None:
    c = F.sum(F.col("amount"))
    assert c._expr == "SUM(`amount`)"


def test_avg() -> None:
    c = F.avg(F.col("price"))
    assert c._expr == "AVG(`price`)"


def test_min() -> None:
    c = F.min(F.col("date"))
    assert c._expr == "MIN(`date`)"


def test_max() -> None:
    c = F.max(F.col("score"))
    assert c._expr == "MAX(`score`)"


def test_coalesce() -> None:
    c = F.coalesce(F.col("a"), F.col("b"), F.lit(0))
    assert c._expr == "COALESCE(`a`, `b`, 0)"


def test_concat() -> None:
    c = F.concat(F.col("first"), F.lit(" "), F.col("last"))
    assert c._expr == "CONCAT(`first`, ' ', `last`)"


def test_upper() -> None:
    c = F.upper(F.col("name"))
    assert c._expr == "UPPER(`name`)"


def test_lower() -> None:
    c = F.lower(F.col("name"))
    assert c._expr == "LOWER(`name`)"


def test_length() -> None:
    c = F.length(F.col("text"))
    assert c._expr == "LENGTH(`text`)"


def test_trim() -> None:
    c = F.trim(F.col("name"))
    assert c._expr == "TRIM(`name`)"


def test_abs() -> None:
    c = F.abs(F.col("value"))
    assert c._expr == "ABS(`value`)"


def test_round() -> None:
    c = F.round(F.col("price"), 2)
    assert c._expr == "ROUND(`price`, 2)"


def test_current_date() -> None:
    c = F.current_date()
    assert c._expr == "CURRENT_DATE"


def test_current_timestamp() -> None:
    c = F.current_timestamp()
    assert c._expr == "CURRENT_TIMESTAMP"


def test_year_month_day() -> None:
    assert F.year(F.col("d"))._expr == "YEAR(`d`)"
    assert F.month(F.col("d"))._expr == "MONTH(`d`)"
    assert F.day(F.col("d"))._expr == "DAY(`d`)"


def test_alias() -> None:
    c = F.alias(F.col("salary"), "sal")
    assert c._expr == "`salary` AS `sal`"


def test_asc_desc() -> None:
    assert F.asc(F.col("name"))._expr == "`name` ASC"
    assert F.desc(F.col("name"))._expr == "`name` DESC"
