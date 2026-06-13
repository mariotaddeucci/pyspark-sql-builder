from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.column import Column


def test_col() -> None:
    """
    PySpark docstring example:
    >>> col('x')
    Column<'x'>
    >>> column('x')
    Column<'x'>
    """
    c = F.col("id")
    assert isinstance(c, Column)
    assert c._expr == "`id`"


def test_col_alias() -> None:
    """
    PySpark docstring example:
    >>> df.select(col("id").alias("num")).show()
    """
    c = F.col("id").alias("num")
    assert c._expr == "`id` AS `num`"
