"""Catalog API for accessing database and table metadata.

Mirrors PySpark's pyspark.sql.Catalog API.
See: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Catalog.html
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from polyglot_sql import Table, parse_one

if TYPE_CHECKING:
    from pyspark_sql_builder.session import SparkSession


class AnalysisExceptionError(Exception):
    """Exception raised for analysis errors matching PySpark's AnalysisException.

    This exception is raised when there are issues analyzing a SQL query,
    such as referencing non-existent tables or invalid column references.

    Mirrors: pyspark.errors.exceptions.captured.AnalysisException
    """

    def __init__(self, message: str, error_class: str | None = None) -> None:
        """Initialize AnalysisExceptionError.

        Args:
            message: The error message.
            error_class: Optional error class identifier (e.g.,
                "TABLE_OR_VIEW_NOT_FOUND").
        """
        super().__init__(message)
        self.message = message
        self.error_class = error_class


class Row(dict):
    """A row in a result set.

    Behaves like a dictionary but allows attribute access to fields.
    Example: row['name'] or row.name both work.
    """

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(f"No attribute {key}") from e

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

    def __repr__(self) -> str:
        return f"Row({dict.__repr__(self)})"


class Catalog:
    """Catalog interface for accessing database and table metadata.

    Provides methods to list databases, tables, and get the current database.
    """

    def __init__(self, session: SparkSession) -> None:
        self._session = session

    def currentDatabase(self) -> str:
        """Returns the current database name.

        For PySpark, this would return "default" for Spark SQL.
        For DuckDB, returns the database catalog name (filename-based).
        For SQLite, returns "main".

        Returns:
            The name of the current database.
        """
        dialect = self._session.target_dialect

        if dialect == "duckdb":
            # For DuckDB, query the current database from information_schema
            driver = self._session._get_driver()
            try:
                result = driver.query(
                    "SELECT DISTINCT table_catalog "
                    "FROM information_schema.tables LIMIT 1"
                )
                table = result.read_all()
                if len(table) > 0:
                    catalogs = table.column("table_catalog").to_pylist()
                    if catalogs:
                        return catalogs[0]
            except Exception:
                pass
            # Fallback to main if no tables exist
            return "main"
        elif dialect == "sqlite":
            # SQLite uses "main" as the default database
            return "main"
        else:
            # Spark SQL default
            return "default"

    def listDatabases(self) -> list[Row]:
        """Lists all databases available.

        Returns a list of Row objects with fields: name, description (optional).

        Returns:
            A list of Row objects representing databases.
        """
        dialect = self._session.target_dialect

        if dialect == "duckdb":
            return self._list_databases_duckdb()
        elif dialect == "sqlite":
            return self._list_databases_sqlite()
        else:
            raise NotImplementedError(
                f"listDatabases not implemented for dialect '{dialect}'"
            )

    def listTables(self, db_name: str | None = None) -> list[Row]:
        """Lists all tables in the specified database.

        If db_name is None, uses the current database.

        Args:
            db_name: Database name. If None, uses currentDatabase().

        Returns:
            A list of Row objects representing tables, with fields:
            name, database, description, tableType, isTemporary.
        """
        if db_name is None:
            db_name = self.currentDatabase()

        dialect = self._session.target_dialect

        if dialect == "duckdb":
            return self._list_tables_duckdb(db_name)
        elif dialect == "sqlite":
            return self._list_tables_sqlite(db_name)
        else:
            raise NotImplementedError(
                f"listTables not implemented for dialect '{dialect}'"
            )

    def tableExists(self, table_name: str) -> bool:
        """Check if a table exists in the current database.

        Performs a single query to list all tables, then checks if the given
        table is in the result set (more efficient than checking one table
        at a time).

        Args:
            table_name: The name of the table to check.

        Returns:
            True if the table exists, False otherwise.
        """
        tables = self.listTables()
        table_names = {t.name for t in tables}
        return table_name in table_names

    def _extract_tables_from_query(self, query: str) -> set[str]:
        """Extract all table names referenced in a SQL query using polyglot AST.

        Uses polyglot-sql's parse_one to analyze the query's AST and extract
        all Table references in a single pass, including subqueries and CTEs.

        Args:
            query: SQL query string.

        Returns:
            Set of table names referenced in the query.
        """
        try:
            parsed = parse_one(query)
            # Find all Table nodes in the AST
            tables = {table.name for table in parsed.find_all(Table)}
            return tables
        except Exception:
            # If parsing fails, return empty set
            # The actual query execution will surface any errors
            return set()

    def verify_tables_exist(self, query: str, db_name: str | None = None) -> None:
        """Verify that all tables referenced in a query exist in the database.

        Extracts all table names from the query using AST analysis, then
        performs a single catalog lookup to verify all tables exist. This is
        more efficient than executing the query and letting the database error.

        Args:
            query: SQL query to verify.
            db_name: Database name. If None, uses currentDatabase().

        Raises:
            AnalysisExceptionError: If any referenced table doesn't exist.
        """
        if db_name is None:
            db_name = self.currentDatabase()

        # Extract all tables from the query in a single AST pass
        referenced_tables = self._extract_tables_from_query(query)

        if not referenced_tables:
            # If no tables found, query is valid (e.g., SELECT 1)
            return

        # Get all available tables in a single catalog query
        available_tables = self.listTables(db_name)
        available_table_names = {t.name for t in available_tables}

        # Find missing tables
        missing_tables = referenced_tables - available_table_names

        if missing_tables:
            # Raise exception for the first missing table (matching PySpark
            # behavior)
            missing_table = sorted(missing_tables)[0]
            raise AnalysisExceptionError(
                f"Table or view '{missing_table}' not found in database '{db_name}'",
                error_class="TABLE_OR_VIEW_NOT_FOUND",
            )

    def _list_databases_duckdb(self) -> list[Row]:
        """Get list of databases from DuckDB."""
        driver = self._session._get_driver()

        # Query DuckDB's system view for databases
        # DuckDB has a special function duckdb_databases() that lists all databases
        query = "SELECT database_name AS name FROM duckdb_databases()"

        reader = driver.query(query)
        table = reader.read_all()

        rows = []
        for record_batch in [table]:
            names = record_batch.column("name").to_pylist()
            for name in names:
                rows.append(Row(name=name, description=None))

        return rows

    def _list_databases_sqlite(self) -> list[Row]:
        """Get list of databases from SQLite.

        SQLite has limited metadata support. We'll return 'main' as the
        default database.
        """
        # SQLite only has "main" database in most cases
        return [Row(name="main", description=None)]

    def _list_tables_duckdb(self, dbName: str) -> list[Row]:
        """Get list of tables from DuckDB for a specific database."""
        driver = self._session._get_driver()

        # Query DuckDB using information_schema.tables
        # Filter by table_catalog to get tables in the specific database
        query = f"""
        SELECT
            table_name AS name,
            table_catalog AS database,
            NULL AS description,
            'EXTERNAL' AS tableType,
            FALSE AS isTemporary
        FROM information_schema.tables
        WHERE table_catalog = '{dbName}'
        AND table_schema = 'main'
        ORDER BY table_name
        """

        reader = driver.query(query)
        table = reader.read_all()

        rows = []
        if len(table) > 0:
            names = table.column("name").to_pylist()
            databases = table.column("database").to_pylist()
            descriptions = table.column("description").to_pylist()
            table_types = table.column("tableType").to_pylist()
            is_temp = table.column("isTemporary").to_pylist()

            for name, db, desc, ttype, temp in zip(
                names, databases, descriptions, table_types, is_temp
            ):
                rows.append(
                    Row(
                        name=name,
                        database=db,
                        description=desc,
                        tableType=ttype,
                        isTemporary=bool(temp),
                    )
                )

        return rows

    def _list_tables_sqlite(self, dbName: str) -> list[Row]:
        """Get list of tables from SQLite for a specific database."""
        driver = self._session._get_driver()

        # SQLite's master table lists all tables and views
        query = """
        SELECT
            name,
            CASE WHEN type='view' THEN 'VIEW' ELSE 'EXTERNAL' END AS tableType,
            0 AS isTemporary
        FROM sqlite_master
        WHERE type IN ('table', 'view')
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """

        reader = driver.query(query)
        table = reader.read_all()

        rows = []
        for batch in [table]:
            names = batch.column("name").to_pylist()
            table_types = batch.column("tableType").to_pylist()
            is_temp = batch.column("isTemporary").to_pylist()

            for name, ttype, temp in zip(names, table_types, is_temp):
                rows.append(
                    Row(
                        name=name,
                        database=dbName,
                        description=None,
                        tableType=ttype,
                        isTemporary=bool(temp),
                    )
                )

        return rows
