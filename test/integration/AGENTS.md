# Integration Test Guide — pyspark-sql-builder

## Fixtures

- `spark` — parametrized over all dialects in `params`. Runs each test against every engine. Automatically skips tests when referenced tables are missing (via AnalysisException).

## Automatic Skip by Table Availability (AnalysisException)

Tests are **automatically skipped** when they try to access non-existent tables:

1. Test calls `df.toArrow()` or similar method
2. `DataFrame.toArrow()` calls `catalog.verify_tables_exist(query)` before executing
3. If a table is missing, `AnalysisException` is raised with `error_class="TABLE_OR_VIEW_NOT_FOUND"`
4. The `spark` fixture catches this exception and converts it to `pytest.skip()`
5. Test is skipped **on that dialect only** — other dialects still run

## Principle

Every integration test must verify that for **each engine** the test runs on, the query result — materialised as a `pyarrow.Table` via `df.toArrow()` → `to_pylist()` — returns **identical data**. This guarantees cross-engine consistency of the generated SQL.

When a test references a table that doesn't exist in an engine:
- The `Catalog.verify_tables_exist()` method analyzes the SQL using polyglot-sql AST
- It extracts all table names and checks them against the dialect's catalog
- If a table is missing, `AnalysisException` is raised (matching PySpark's behavior)
- The fixture automatically converts this to `pytest.skip()`
- Result: **No need for dialect-specific if-statements in tests**

## Adding table data for a specific dialect

Edit the corresponding `assets/<dialect>.sql` file. DuckDB-specific types (STRUCT, TEXT[], etc.) go in `assets/duckdb.sql` only. Tests that query them should reference those tables — the skip mechanism handles missing tables automatically:

```python
def test_complex_query(spark: SparkSession) -> None:
    # This table only exists in duckdb.sql
    result = spark.table("events").select(...)
    
    # For SQLite: toArrow() → AnalysisException → pytest.skip()
    # For DuckDB: proceeds normally
    data = result.toArrow().to_pylist()
```

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
5. **No need for dialect checks** — automatic skip handles missing tables

## Under the Hood

- **Catalog API**: `SparkSession.catalog.verify_tables_exist(query)` uses polyglot-sql's `parse_one()` to extract all referenced tables from the SQL AST in a single pass
- **AnalysisException**: PySpark-compatible exception class matching `pyspark.errors.exceptions.captured.AnalysisException`
- **Fixture Integration**: The `spark` fixture wraps test execution to catch `AnalysisException` with `error_class="TABLE_OR_VIEW_NOT_FOUND"` and automatically calls `pytest.skip()`
- **Efficiency**: One AST parse + one catalog query per test (not N queries for N tables)

