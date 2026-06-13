"""PySpark SQL Builder package.

Provides a PySpark-compatible SQL API for building and executing SQL queries
using various database backends.
"""

# Main public API
from pyspark_sql_builder.pyspark.exceptions import AnalysisExceptionError
from pyspark_sql_builder.pyspark.sql import (
    Catalog,
    Column,
    DataFrame,
    GroupedData,
    Row,
    SparkSession,
    Window,
    functions,
    types,
)

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
