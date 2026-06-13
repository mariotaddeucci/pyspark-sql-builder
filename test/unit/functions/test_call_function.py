from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_call_function_no_args() -> None:
    c = F.call_function("my_func")
    assert c._expr == "my_func()"


def test_call_function_with_args() -> None:
    c = F.call_function("my_func", F.col("a"), F.lit(1))
    assert c._expr == "my_func(`a`, 1)"


def test_call_function_mixed() -> None:
    c = F.call_function("my_func", F.col("a"), "hello", None)
    assert c._expr == "my_func(`a`, 'hello', NULL)"
