# pyspark-sql-builder — Agent Guide

## Commands

```bash
prek run --all-files                    # ruff fix → ruff format → pyrefly check (order matters)
uv run pytest -v                        # all tests
uv run pytest test/unit/ -v             # unit only
uv run pytest test/integration/ -v      # integration only (uses SQLite)
uv run pytest -k "transpile"            # filter
uv run pytest --cov --cov-report=term   # coverage (terminal)
uv run pytest --cov --cov-report=html   # coverage (HTML)
```

## Architecture

```
src/pyspark_sql_builder/
├── session.py      # SparkSession (+ Builder), entry point. Exceptions: read, write, range, destroy, sql
├── dataframe.py    # DataFrame: wraps SQL string in _query, _wrap() returns new instance
├── column.py       # Column: wraps expression in _expr, _quote_ident(), _to_expr()
├── functions.py    # col, lit, count, sum, when, row_number, 60+ SQL function constructors
├── group.py        # GroupedData: groupBy().agg() + count/sum/avg/min/max
├── window.py       # Window: partitionBy/orderBy, via Column.over()
├── readwriter.py   # DataFrameReader / DataFrameWriter stubs
├── drivers.py      # DatabaseDriver ABC, DuckDBDriver, ConnectorXDriver
└── types.py        # DataType, StringType, StructType, ArrayType, MapType, DecimalType, etc.
```

## PySpark API conformance (MANDATORY)

All public API for **DataFrame**, **Column**, **functions**, **Window**, **Reader**, **Writer** must mirror the official PySpark API exactly — same method names, signatures, and behavior. **No extra methods, no missing methods, no signature deviations.** Before implementing or when in doubt, consult:
<https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/index.html>

Exception: `SparkSession` may contain driver-connection helpers and constructor patterns (`SparkSession.builder.config(...).getOrCreate()`, `SparkSession(connection="...", dialect="...")`) to pass context — the rest must follow PySpark.

**Validation**: The `functions` module shadows Python builtins (`sum`, `min`, `max`, `abs`, `round`). Use `from pyspark_sql_builder import functions as F` and access via `F.sum()` etc.

## Design rules

- **`generate_query(dialect=None)`** is the output method. Builds SQL from `self._query`, transpiles with `polyglot_sql`. Fast-paths `"spark"` (no transpilation).
- **DataFrame wrapping**: every transformation method returns a new `DataFrame` via `_wrap(sql)` or `_replace_select(cols)` — never mutates in-place.
- **Column stores `_expr`** (raw SQL fragment), not a column name. `name` property strips backticks from each dot-separated part.
- **`Column.__eq__` returns `Column`** (not `bool`), like PySpark. Never use `==` in Python if-branches with Column; compare `_expr` instead.
- **`_to_expr(value)`** converts Python values to SQL literals: `str → 'quoted'`, `None → NULL`, `bool → TRUE/FALSE`, `Column → its _expr`.
- **Auto-backtick identifiers**: `F.col("x")`, `.select("x")`, `.groupBy("x")`, `.orderBy("x")`, `.join(using=list)` all quote via `_quote_ident()`. `selectExpr(string)` and raw `Column("sql")` pass through unquoted.
- **`Column.name` strips backticks**: used for matching in `withColumn()`, `withColumnRenamed()`, `drop()`. Compare with `c.name`, not `c._expr`.
- **`join()` with `list[str]`** produces `JOIN ... USING (col1, col2)`.
- **Window functions**: `F.sum(F.col("x")).over(Window.partitionBy("y").orderBy("z"))`.
- **`GroupedData` breaks circular import** via `TYPE_CHECKING` + lazy `from pyspark_sql_builder.dataframe import DataFrame as _DataFrame` inside `agg()`.
- **`SparkSession` exceptions** (deviation from PySpark): accepts `connection` and `dialect` kwargs; has `target_dialect` prop; `to_arrow_reader(query)` for execution; `range()` exists as a convenience. `read`/`writer` properties return stubs.

## Design principles

- **No silent unsupported behavior**: If a Spark API parameter has no equivalent or cannot be implemented for the target format/driver, raise `ValueError` with a clear message — never silently ignore.
- **Streaming-first, no materialization**: Always use `RecordBatchReader` / lazy iteration. Never call `read_all()`, `to_pylist()`, `to_pydict()`, or otherwise materialize the full dataset in memory. Data must flow through Arrow zero-copy wherever possible.
- **Explicit over implicit**: If a codec, option, or format is not supported, the user must be told immediately via an exception. Silent fallbacks or no-ops lead to confusion and data loss.

## Config

- **Build**: `uv_build` (not setuptools)
- **Ruff**: select `E,F,I,W,N,UP`, ignore `N802` (camelCase methods) and `N812` (functions shadowing builtins as `F`)
- **Type checker**: pyrefly (not pyright)
- **pre-commit**: `prek install` → hooks run `ruff fix → ruff format → pyrefly check`
