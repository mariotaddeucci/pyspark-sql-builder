from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_input_file_name() -> None:
    c = F.input_file_name()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
