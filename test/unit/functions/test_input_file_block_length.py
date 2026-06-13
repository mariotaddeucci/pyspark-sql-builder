from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_input_file_block_length() -> None:
    c = F.input_file_block_length()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
