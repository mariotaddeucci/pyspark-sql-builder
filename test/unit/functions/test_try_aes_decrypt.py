from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_try_aes_decrypt() -> None:
    c = F.try_aes_decrypt(F.col("x"), "key")
    assert c._expr == "TRY_AES_DECRYPT(`x`, 'key')"
