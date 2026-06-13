# Integration Test Guide — pyspark-sql-builder

## Fixtures

- `spark` — parametrized over `sqlite` and `duckdb`. Runs each test against both engines.
- `duckdb_spark` — wraps `spark` and **skips at fixture level** when dialect is not `duckdb`. Use for structs, arrays, explode, date functions, `range()`, or any DuckDB-only feature.

## Principle

Every integration test must verify that for **each engine** the test runs on, the query result — materialised as a `pyarrow.Table` via `df.toArrow()` → `to_pylist()` — returns **identical data**. This guarantees cross-engine consistency of the generated SQL.

Example:
```python
def test_something(duckdb_spark: SparkSession) -> None:
    result = duckdb_spark.table("t").select(...).orderBy(...)
    data = result.toArrow().to_pylist()
    assert data == [{"col": value, ...}, ...]
```

## Dialect-level skip

DuckDB-only tests use the `duckdb_spark` fixture. The skip happens **in the fixture** (before the test body runs), not inside the test. If a test can run on both dialects, it uses the `spark` fixture directly.

To add a new dialect-specific fixture, add a `_check_dialect` call in `conftest.py`.

## Adding table data for a specific dialect

Edit the corresponding `assets/<dialect>.sql` file. DuckDB-specific types (STRUCT, TEXT[], etc.) go in `assets/duckdb.sql` only. Tests that query them must use `duckdb_spark`.

## Running

```bash
uv run pytest test/integration/ -v        # all integration tests
uv run pytest test/integration/ -k duckdb  # DuckDB only
uv run pytest test/integration/ -k sqlite  # SQLite only
```

## Test pattern

1. Build a query with the PySpark API chaining
2. Call `.toArrow().to_pylist()` (or check `.columns`, `.dtypes`, `.schema`)
3. Assert on the exact list of dicts or metadata
4. Every assertion value must be deterministic (avoid `RAND()`, `CURRENT_DATE`, etc.)
