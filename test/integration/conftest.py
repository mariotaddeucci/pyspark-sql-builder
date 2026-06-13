from __future__ import annotations

import re
from collections.abc import Generator
from pathlib import Path

import pytest

from pyspark_sql_builder.session import SparkSession

_CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)", re.IGNORECASE
)


def _tables_in_asset(dialect: str) -> set[str]:
    path = Path(__file__).parent / "assets" / f"{dialect}.sql"
    if not path.exists():
        return set()
    return set(_CREATE_TABLE_RE.findall(path.read_text()))


@pytest.fixture(
    params=[
        pytest.param("sqlite", id="sqlite"),
        pytest.param("duckdb", id="duckdb"),
    ]
)
def spark(request, tmp_path: Path) -> Generator[SparkSession, None, None]:
    dialect: str = request.param

    marker = request.node.get_closest_marker("requires_tables")
    if marker:
        required = set(marker.args)
        existing = _tables_in_asset(dialect)
        missing = required - existing
        if missing:
            pytest.skip(
                f"Tables not defined in assets/{dialect}.sql: "
                f"{', '.join(sorted(missing))}"
            )

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

    yield session
