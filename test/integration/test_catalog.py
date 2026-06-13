"""Integration tests for the Catalog API."""

from __future__ import annotations

import pytest

from pyspark_sql_builder.pyspark.exceptions import AnalysisExceptionError
from pyspark_sql_builder.pyspark.sql.session import SparkSession


def test_current_database(spark: SparkSession) -> None:
    """Test currentDatabase returns the database name."""
    db = spark.catalog.currentDatabase()
    assert isinstance(db, str)
    assert db


def test_list_databases(spark: SparkSession) -> None:
    """Test listDatabases returns a list of database rows."""
    databases = spark.catalog.listDatabases()
    assert isinstance(databases, list)
    assert len(databases) >= 1

    for db_row in databases:
        assert hasattr(db_row, "name")
        assert isinstance(db_row.name, str)
        assert db_row.name
        assert hasattr(db_row, "description")


def test_list_tables(spark: SparkSession) -> None:
    """Test listTables returns a list of table rows."""
    tables = spark.catalog.listTables()
    assert isinstance(tables, list)
    assert len(tables) >= 4

    for table_row in tables:
        assert hasattr(table_row, "name")
        assert isinstance(table_row.name, str)
        assert table_row.name

        assert hasattr(table_row, "database")
        assert isinstance(table_row.database, str)

        assert hasattr(table_row, "tableType")
        assert table_row.tableType in ("EXTERNAL", "VIEW")

        assert hasattr(table_row, "isTemporary")
        assert isinstance(table_row.isTemporary, bool)


def test_list_tables_with_explicit_database(spark: SparkSession) -> None:
    """Test listTables works with explicit database parameter."""
    current_db = spark.catalog.currentDatabase()
    tables = spark.catalog.listTables(current_db)

    assert isinstance(tables, list)
    assert len(tables) >= 4

    for table_row in tables:
        assert table_row.database == current_db


def test_list_tables_contains_expected_tables(spark: SparkSession) -> None:
    """Test listTables includes expected tables."""
    tables = spark.catalog.listTables()
    table_names = {t.name for t in tables}

    expected_tables = {"users", "regions", "transactions", "categories"}
    assert expected_tables.issubset(table_names), (
        f"Missing tables: {expected_tables - table_names}"
    )


def test_row_dict_access(spark: SparkSession) -> None:
    """Test Row objects support dict and attribute access."""
    databases = spark.catalog.listDatabases()

    for db in databases:
        assert db["name"] == db.name
        assert db["description"] == db.description


def test_table_exists_single_table(spark: SparkSession) -> None:
    """Test tableExists for single table."""
    assert spark.catalog.tableExists("users") is True
    assert spark.catalog.tableExists("transactions") is True
    assert spark.catalog.tableExists("nonexistent_table") is False


def test_table_exists_multiple_tables(spark: SparkSession) -> None:
    """Test tableExists returns correct results."""
    assert spark.catalog.tableExists("users") is True
    assert spark.catalog.tableExists("regions") is True
    assert spark.catalog.tableExists("categories") is True

    assert spark.catalog.tableExists("fake_table") is False
    assert spark.catalog.tableExists("missing_table") is False


def test_verify_tables_exist_simple_query(spark: SparkSession) -> None:
    """Test verify_tables_exist with simple query."""
    spark.catalog.verify_tables_exist("SELECT * FROM users")
    spark.catalog.verify_tables_exist("SELECT * FROM transactions WHERE user_id = 1")


def test_verify_tables_exist_multiple_tables(spark: SparkSession) -> None:
    """Test verify_tables_exist with multiple tables."""
    spark.catalog.verify_tables_exist(
        "SELECT * FROM users JOIN transactions ON users.id = transactions.user_id"
    )


def test_verify_tables_exist_with_subquery(spark: SparkSession) -> None:
    """Test verify_tables_exist extracts tables from subqueries."""
    spark.catalog.verify_tables_exist(
        "SELECT * FROM users WHERE id IN (SELECT user_id FROM transactions)"
    )


def test_verify_tables_exist_missing_table(spark: SparkSession) -> None:
    """Test verify_tables_exist raises exception for missing table."""
    with pytest.raises(AnalysisExceptionError) as exc_info:
        spark.catalog.verify_tables_exist("SELECT * FROM nonexistent_table")

    assert "nonexistent_table" in str(exc_info.value)
    assert exc_info.value.error_class == "TABLE_OR_VIEW_NOT_FOUND"


def test_verify_tables_exist_missing_table_in_subquery(spark: SparkSession) -> None:
    """Test verify_tables_exist detects missing tables in subqueries."""
    with pytest.raises(AnalysisExceptionError) as exc_info:
        spark.catalog.verify_tables_exist(
            "SELECT * FROM users WHERE id IN (SELECT user_id FROM missing_table)"
        )

    assert "missing_table" in str(exc_info.value)


def test_verify_tables_exist_multiple_missing_tables(spark: SparkSession) -> None:
    """Test verify_tables_exist with multiple missing tables."""
    with pytest.raises(AnalysisExceptionError) as exc_info:
        spark.catalog.verify_tables_exist(
            "SELECT * FROM missing1 JOIN missing2 ON missing1.id = missing2.id"
        )

    assert "missing1" in str(exc_info.value) or "missing2" in str(exc_info.value)


def test_verify_tables_exist_query_without_tables(spark: SparkSession) -> None:
    """Test verify_tables_exist with query without tables."""
    spark.catalog.verify_tables_exist("SELECT 1")
    spark.catalog.verify_tables_exist("SELECT 1 + 2 AS result")
    spark.catalog.verify_tables_exist("SELECT CURRENT_DATE()")


def test_table_not_found_exception_message(spark: SparkSession) -> None:
    """Test AnalysisExceptionError message format."""
    try:
        spark.catalog.verify_tables_exist("SELECT * FROM nonexistent_table")
    except AnalysisExceptionError as e:
        assert "[TABLE_OR_VIEW_NOT_FOUND]" in str(e) or "nonexistent_table" in str(e)
        assert "nonexistent_table" in str(e)
        assert e.error_class == "TABLE_OR_VIEW_NOT_FOUND"


def test_automatic_skip_on_missing_table_in_dataframe(spark: SparkSession) -> None:
    """Test toArrow raises AnalysisException for missing tables."""
    df = spark.table("nonexistent_table")

    with pytest.raises(AnalysisExceptionError) as exc_info:
        df.toArrow()

    assert exc_info.value.error_class == "TABLE_OR_VIEW_NOT_FOUND"
    assert "nonexistent_table" in str(exc_info.value)


def test_automatic_skip_on_missing_table_in_join(spark: SparkSession) -> None:
    """Test automatic skip works for missing tables in joins."""
    df = spark.table("users").join(
        "nonexistent_table", "users.id = nonexistent_table.user_id"
    )

    with pytest.raises(AnalysisExceptionError) as exc_info:
        df.toArrow()

    assert exc_info.value.error_class == "TABLE_OR_VIEW_NOT_FOUND"
    assert "nonexistent_table" in str(exc_info.value)
