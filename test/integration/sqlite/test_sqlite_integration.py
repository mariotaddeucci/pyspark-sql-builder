import sqlite3

import pytest

from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession


@pytest.fixture()
def spark() -> SparkSession:
    return SparkSession(dialect="sqlite")


def test_join_agg_order(
    spark: SparkSession,
    sqlite_conn: sqlite3.Connection,
) -> None:
    result = (
        spark.table("transactions")
        .join("users", F.col("transactions.user_id") == F.col("users.id"))
        .select(
            F.col("users.email"),
            F.col("transactions.amount"),
            F.col("transactions.date"),
        )
        .groupBy(F.col("users.email"), F.col("transactions.date"))
        .agg(F.sum(F.col("amount")).alias("balance"))
        .orderBy(F.col("users.email"), F.col("transactions.date"))
    )
    query = result.generate_query()
    assert query

    cursor = sqlite_conn.execute(query)
    rows = cursor.fetchall()
    assert len(rows) == 7

    r1, r2, r3, r4, r5, r6, r7 = rows
    assert r1["email"] == "joao@email.com"
    assert r1["date"] == "2024-01-01"
    assert r1["balance"] == 100.0

    assert r2["email"] == "joao@email.com"
    assert r2["date"] == "2024-01-15"
    assert r2["balance"] == -50.0

    assert r3["email"] == "joao@email.com"
    assert r3["date"] == "2024-02-20"
    assert r3["balance"] == 25.0

    assert r4["email"] == "maria@email.com"
    assert r4["date"] == "2024-02-01"
    assert r4["balance"] == 200.0

    assert r5["email"] == "maria@email.com"
    assert r5["date"] == "2024-02-15"
    assert r5["balance"] == -30.0

    assert r6["email"] == "maria@email.com"
    assert r6["date"] == "2024-03-01"
    assert r6["balance"] == 80.0

    assert r7["email"] == "pedro@email.com"
    assert r7["date"] == "2024-01-10"
    assert r7["balance"] == 500.0


def test_reserved_word_columns(
    spark: SparkSession,
    sqlite_conn: sqlite3.Connection,
) -> None:
    sqlite_conn.executescript("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            "order" INTEGER NOT NULL,
            "group" TEXT NOT NULL,
            "from" TEXT NOT NULL
        );
        INSERT INTO events (id, "order", "group", "from") VALUES
            (1, 10, 'admin', 'nyc'),
            (2, 20, 'user', 'sf');
    """)

    df = (
        spark.table("events")
        .select("id", "order", "group", "from")
        .where(F.col("order") > 15)
    )
    query = df.generate_query()
    assert query

    cursor = sqlite_conn.execute(query)
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0]["id"] == 2
    assert rows[0]["order"] == 20
    assert rows[0]["group"] == "user"
    assert rows[0]["from"] == "sf"


def test_multiple_filters_and_aggregates(
    spark: SparkSession,
    sqlite_conn: sqlite3.Connection,
) -> None:
    result = (
        spark.table("transactions")
        .join("users", F.col("transactions.user_id") == F.col("users.id"))
        .select(
            F.col("users.name"),
            F.col("users.email"),
            F.col("transactions.amount"),
        )
        .where(F.col("transactions.amount") > 0)
        .where(F.col("users.email").like("%@email.com"))
        .groupBy(F.col("users.email"), F.col("users.name"))
        .agg(
            F.sum(F.col("amount")).alias("total"),
            F.count(F.col("amount")).alias("count"),
            F.max(F.col("amount")).alias("max_amount"),
        )
        .orderBy(F.col("total").desc())
    )
    query = result.generate_query()
    assert query

    cursor = sqlite_conn.execute(query)
    rows = cursor.fetchall()
    assert len(rows) == 3

    r1, r2, r3 = rows
    assert r1["email"] == "pedro@email.com"
    assert r1["total"] == 500.0
    assert r1["count"] == 1
    assert r1["max_amount"] == 500.0

    assert r2["email"] == "maria@email.com"
    assert r2["total"] == 280.0
    assert r2["count"] == 2
    assert r2["max_amount"] == 200.0

    assert r3["email"] == "joao@email.com"
    assert r3["total"] == 125.0
    assert r3["count"] == 2
    assert r3["max_amount"] == 100.0
