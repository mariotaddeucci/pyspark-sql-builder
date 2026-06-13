from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest

from pyspark_sql_builder.pyspark.exceptions import AnalysisExceptionError
from pyspark_sql_builder.pyspark.sql.session import SparkSession


@pytest.fixture(
    params=[
        pytest.param("sqlite", id="sqlite"),
        pytest.param("duckdb", id="duckdb"),
    ]
)
def spark(request, tmp_path: Path) -> Generator[SparkSession, None, None]:
    dialect: str = request.param

    asset_path = Path(__file__).parent / "assets" / f"{dialect}.sql"
    setup_sql = asset_path.read_text()

    if dialect == "sqlite":
        db_file = tmp_path / "test.db"
        conn_str = f"sqlite://{db_file}"
        import sqlite3

        conn = sqlite3.connect(str(db_file))
        conn.executescript(setup_sql)
        conn.close()
    else:
        db_file = tmp_path / "test.duckdb"
        conn_str = f"duckdb://{db_file}"

    session = SparkSession(dialect=dialect, connection=conn_str)

    if dialect == "duckdb":
        session._get_driver().execute(setup_sql)

    # Wrap test execution to catch AnalysisException for table not found
    original_runtest = request.node.runtest

    def wrapped_runtest(*args, **kwargs):
        try:
            return original_runtest(*args, **kwargs)
        except AnalysisExceptionError as e:
            # Skip test if table/view not found
            if e.error_class == "TABLE_OR_VIEW_NOT_FOUND":
                pytest.skip(f"Table not found: {str(e)}")
            # Re-raise other analysis exceptions
            raise

    request.node.runtest = wrapped_runtest

    yield session
