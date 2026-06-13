from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_lit_int() -> None:
    """
    PySpark docstring Example 1:
    >>> df.select(sf.lit(5).alias('height'), df.id).show()
    """
    c = F.lit(5)
    assert c._expr == "5"


def test_lit_string() -> None:
    """
    PySpark docstring Example 3:
    >>> df.select(sf.lit("PySpark").alias('framework'), df.id).show()
    """
    c = F.lit("PySpark")
    assert c._expr == "'PySpark'"


def test_lit_bool() -> None:
    """
    PySpark docstring Example 4:
    >>> df.select(sf.lit(False).alias('is_approved'), df.response).show()
    """
    c = F.lit(False)
    assert c._expr == "FALSE"


def test_lit_null() -> None:
    """
    PySpark docstring: a literal NULL value.
    """
    c = F.lit(None)
    assert c._expr == "NULL"
