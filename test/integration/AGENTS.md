# Integration Test Guide — pyspark-sql-builder

## Fixtures

- `spark` — parametrized over all dialects in `params`. Runs each test against every engine that has all required tables defined in its asset SQL.

## Skip by table availability

Use `@pytest.mark.requires_tables("table1", "table2")` to declare that a test needs specific tables. The fixture reads the dialect's `assets/<dialect>.sql`, extracts all `CREATE TABLE` names, and **skips at fixture level** if any required table is missing — with zero engine-name hardcoding.

When adding a new dialect:
1. Create `assets/<dialect>.sql` with the `CREATE TABLE` statements the tests need.
2. The `requires_tables` mechanism automatically detects the tables → tests run on that dialect.
3. No need to touch `params` or add conditional `pytest.skip()` logic per dialect.

## Principle

Every integration test must verify that for **each engine** the test runs on, the query result — materialised as a `pyarrow.Table` via `df.toArrow()` → `to_pylist()` — returns **identical data**. This guarantees cross-engine consistency of the generated SQL.

Example:
```python
import pytest
from pyspark_sql_builder import functions as F
from pyspark_sql_builder.session import SparkSession

@pytest.mark.requires_tables("users", "transactions")
def test_something(spark: SparkSession) -> None:
    result = spark.table("users").select(...).orderBy(...)
    data = result.toArrow().to_pylist()
    assert data == [{"col": value, ...}, ...]
```

## Adding table data for a specific dialect

Edit the corresponding `assets/<dialect>.sql` file. DuckDB-specific types (STRUCT, TEXT[], etc.) go in `assets/duckdb.sql` only. Tests that query them must use `@pytest.mark.requires_tables("events")`.

## Running

```bash
uv run pytest test/integration/ -v                         # all integration tests
uv run pytest test/integration/ -k "not SKIPPED"           # non-skipped only
uv run test/integration/ -v --co                         # with output
```

## Test pattern

1. Build a query with the PySpark API chaining
2. Call `.toArrow().to_pylist()` (or check `.columns`, `.dtypes`, `.schema`)
3. Assert on the exact list of dicts or metadata
4. Every assertion value must be deterministic (avoid `RAND()`, `CURRENT_DATE`, etc.)
5. If the test needs specific tables, add `@pytest.mark.requires_tables(...)`
