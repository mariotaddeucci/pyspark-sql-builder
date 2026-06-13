from __future__ import annotations

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


def test_filter(spark: SparkSession) -> None:
    df = spark.table("users").filter(F.col("active") == True)  # noqa: E712
    assert df.generate_query() == (
        "SELECT * FROM (SELECT * FROM users) AS _t WHERE `active` = TRUE"
    )
