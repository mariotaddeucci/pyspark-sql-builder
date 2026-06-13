from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_alias() -> None:
    """
    PySpark docstring example:
    >>> alias(col("salary"), "sal")
    Returns a column with a new alias.
    """
    c = F.alias(F.col("salary"), "sal")
    assert c._expr == "`salary` AS `sal`"
