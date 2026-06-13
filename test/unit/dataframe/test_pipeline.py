from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_full_pipeline(spark: SparkSession) -> None:
    df = (
        spark.table("orders")
        .join("customers", F.col("orders.customer_id") == F.col("customers.id"))
        .select("orders.id", "customers.name", "orders.amount")
        .where(F.col("orders.amount") > 100)
        .orderBy(F.col("orders.amount").desc())
        .limit(50)
    )
    result = df.generate_query()
    assert "SELECT" in result
    assert "FROM orders" in result
    assert "JOIN customers" in result
    assert "WHERE" in result
    assert "ORDER BY" in result
    assert "LIMIT 50" in result
