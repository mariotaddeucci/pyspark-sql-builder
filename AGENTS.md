# pyspark-sql-builder — Agent Guide

## Commands

```bash
prek run --all-files                    # ruff fix → ruff format → pyrefly check
uv run pytest -v                        # all 105 tests (unit + integration)
uv run pytest test/unit/ -v             # unit only
uv run pytest test/integration/ -v      # SQLite integration only
uv run pytest -k "transpile"            # filter
```

## Architecture

```
src/pyspark_sql_builder/
├── session.py      # SparkSession (+ Builder), entry point
├── dataframe.py    # DataFrame: query state machine, _build_sql(), generate_query(dialect)
├── column.py       # Column: wraps expression string in _expr, _quote_ident(), _to_expr()
├── functions.py    # col, lit, count, sum, when, row_number, 50+ SQL function constructors
├── group.py        # GroupedData: group_by().agg() chaining, lazy DataFrame import
├── window.py       # Window: partitionBy/orderBy, used via Column.over()
├── readwriter.py   # DataFrameReader / DataFrameWriter stubs
└── types.py        # DataType, StringType, StructType, ArrayType, etc.
```

## Design rules

- **`generate_query(dialect=None)`** is the output method. Builds SQL via `_build_sql()`, transpiles with `polyglot_sql.parse_one(sql).sql(dialect=target)`. Fast-paths "spark" (no transpilation).
- **Immutability**: every DataFrame method returns `self._clone()` via `__new__` + field copy.
- **Column stores `_expr`** (raw SQL fragment), not name. `name` is a property that strips backticks from each dot-separated part.
- **`Column.__eq__` returns `Column`** (not `bool`), mimicking PySpark. Never use `==` in Python if-branches with Column; compare `_expr` instead.
- **`_to_expr(value)`** converts Python values to SQL literals: `str → 'quoted'`, `None → NULL`, `bool → TRUE/FALSE`, `Column → its _expr`.
- **Auto-backtick all identifiers**: `F.col()`, `.select(string)`, `.groupBy(string)`, `.orderBy(string)`, `.join(using=list)` all quote via `_quote_ident()`. `selectExpr(string)` and raw `Column("sql")` do NOT quote — they pass through as-is.
- **`Column.name` strips backticks**: used by `withColumn()`, `withColumnRenamed()`, `drop()` for matching. Use `c.name` (not `c._expr`) when comparing against user-provided column names.
- **Window functions**: `F.sum(F.col("x")).over(Window.partitionBy("y").orderBy("z"))`.
- **`join()` with `list[str]`** produces `JOIN ... USING (col1, col2)`.
- **camelCase API**: Methods mirror PySpark exactly (`groupBy`, `orderBy`, `withColumn`, `withColumnRenamed`, `unionAll`, `exceptAll`, `getOrCreate`). Functions shadow builtins (`sum`, `min`, `max`, `abs`, `round`).
- **`GroupedData` breaks circular import** via `TYPE_CHECKING` + lazy `from pyspark_sql_builder.dataframe import DataFrame as _DataFrame` inside `agg()`.
- **Integration tests** use only PySpark API (no `selectExpr`, no raw `Column("sql")`) to verify generated SQL works against SQLite.

## Config

- `uv_build` (not setuptools)
- Ruff: select `E,F,I,W,N,UP`, ignore `N802` (camelCase) and `N812` (functions as `F`)
- Type checker: pyrefly (not pyright)
- prek: `prek install` hooks run `ruff fix → ruff format → pyrefly check` before commit
