from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.column import Column


def test_when_otherwise() -> None:
    """
    PySpark docstring example:
    >>> when(col("age") > 18, "adult").otherwise("minor")
    """
    c = F.when(F.col("age") > 18, "adult").otherwise("minor")
    assert isinstance(c, Column)
    assert c._expr == "CASE WHEN `age` > 18 THEN 'adult' ELSE 'minor' END"


def test_when_chained() -> None:
    """
    PySpark docstring example:
    >>> when(col("age") < 18, "minor")
    ...     .when(col("age") >= 65, "senior")
    ...     .otherwise("adult")
    """
    c = (
        F.when(F.col("age") < 18, "minor")
        .when(F.col("age") >= 65, "senior")
        .otherwise("adult")
    )
    expected = (
        "CASE WHEN `age` < 18 THEN 'minor'"
        " WHEN `age` >= 65 THEN 'senior'"
        " ELSE 'adult' END"
    )
    assert c._expr == expected
