"""PySpark SQL module for pyspark_sql_builder.

This module provides a PySpark-compatible SQL API.
"""

from pyspark_sql_builder.pyspark.exceptions import AnalysisExceptionError
from pyspark_sql_builder.pyspark.sql import functions, types
from pyspark_sql_builder.pyspark.sql.catalog import (
    Catalog,
    Row,
)
from pyspark_sql_builder.pyspark.sql.column import Column
from pyspark_sql_builder.pyspark.sql.dataframe import DataFrame
from pyspark_sql_builder.pyspark.sql.group import GroupedData
from pyspark_sql_builder.pyspark.sql.session import SparkSession
from pyspark_sql_builder.pyspark.sql.window import Window

__all__ = [
    "SparkSession",
    "DataFrame",
    "Column",
    "GroupedData",
    "Catalog",
    "Row",
    "AnalysisExceptionError",
    "functions",
    "types",
    "Window",
]
