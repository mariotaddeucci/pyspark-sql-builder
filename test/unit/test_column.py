from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.column import Column
from pyspark_sql_builder.window import Window


def test_column_name() -> None:
    c = Column("id")
    assert c.name == "id"


def test_column_with_table() -> None:
    c = Column("users.id")
    assert c.name == "users.id"
    assert c._expr == "users.id"


def test_column_alias() -> None:
    c = Column("salary").alias("sal")
    assert "salary AS" in c._expr


def test_asc() -> None:
    c = Column("name").asc()
    assert c._expr == "name ASC"


def test_desc() -> None:
    c = Column("name").desc()
    assert c._expr == "name DESC"


def test_eq() -> None:
    c = Column("age") == 18
    assert c._expr == "age = 18"


def test_eq_column() -> None:
    c = Column("a") == Column("b")
    assert c._expr == "a = b"


def test_neq() -> None:
    c = Column("status") != "active"
    assert c._expr == "status != 'active'"


def test_gt() -> None:
    c = Column("age") > 21
    assert c._expr == "age > 21"


def test_ge() -> None:
    c = Column("age") >= 18
    assert c._expr == "age >= 18"


def test_lt() -> None:
    c = Column("age") < 65
    assert c._expr == "age < 65"


def test_le() -> None:
    c = Column("age") <= 60
    assert c._expr == "age <= 60"


def test_and() -> None:
    c = (Column("age") > 18) & (Column("age") < 65)
    assert "(age > 18 AND age < 65)" in c._expr


def test_or() -> None:
    c = (Column("status") == "active") | (Column("status") == "pending")
    assert "status = 'active' OR status = 'pending'" in c._expr


def test_invert() -> None:
    c = ~(Column("age") > 18)
    assert "NOT" in c._expr


def test_is_null() -> None:
    c = Column("email").isNull()
    assert c._expr == "email IS NULL"


def test_is_not_null() -> None:
    c = Column("email").isNotNull()
    assert c._expr == "email IS NOT NULL"


def test_between() -> None:
    c = Column("age").between(18, 65)
    assert c._expr == "age BETWEEN 18 AND 65"


def test_like() -> None:
    c = Column("name").like("%john%")
    assert c._expr == "name LIKE '%john%'"


def test_cast() -> None:
    c = Column("age").cast("STRING")
    assert c._expr == "CAST(age AS STRING)"


def test_substr() -> None:
    c = Column("name").substr(1, 3)
    assert c._expr == "SUBSTRING(name, 1, 3)"


def test_arithmetic() -> None:
    assert (Column("a") + Column("b"))._expr == "a + b"
    assert (Column("a") - Column("b"))._expr == "a - b"
    assert (Column("a") * Column("b"))._expr == "a * b"
    assert (Column("a") / Column("b"))._expr == "a / b"


def test_window_over_partition_by() -> None:
    w = Window.partitionBy("dept")
    c = F.sum(F.col("salary")).over(w)
    assert c._expr == "SUM(`salary`) OVER (PARTITION BY `dept`)"


def test_window_over_partition_by_order() -> None:
    w = Window.partitionBy("dept").orderBy("salary")
    c = F.sum(F.col("salary")).over(w)
    assert "PARTITION BY" in c._expr
    assert "ORDER BY" in c._expr


def test_window_over_order_by() -> None:
    w = Window.partitionBy().orderBy("date")
    c = F.row_number().over(w)
    assert c._expr == "ROW_NUMBER() OVER (ORDER BY `date`)"


def test_window_multiple_partition() -> None:
    w = Window.partitionBy("year", "month").orderBy(F.col("amount").desc())
    c = F.sum(F.col("value")).over(w)
    assert "PARTITION BY `year`, `month`" in c._expr
    assert "ORDER BY `amount` DESC" in c._expr
