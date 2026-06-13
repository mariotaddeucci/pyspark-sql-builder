from __future__ import annotations

import pytest

from pyspark_sql_builder.pyspark.sql import functions as F


def test_arrow_udtf_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        F.arrow_udtf(lambda x: x)
