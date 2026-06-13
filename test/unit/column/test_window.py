from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.window import Window


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
