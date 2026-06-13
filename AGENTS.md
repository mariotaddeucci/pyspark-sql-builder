# pyspark-sql-builder — Agent Guide

## Overview

PySpark SQL query builder. Mirrors `pyspark.sql` API but produces SQL strings via polyglot-sql transpilation. No Spark cluster.

## Commands

```bash
uv run pytest -v                              # all tests (unit + integration)
uv run pytest test/unit/ -v                   # unit tests only
uv run pytest test/integration/ -v            # integration tests only
uv run pytest test/unit/test_column.py -v     # single file
uv run pytest -k "transpile"                  # filter
uv run ruff check src/ test/                  # lint
uv run pyrefly check src/                     # type check (preferred)
uv run pytest                                 # test after lint+typecheck
```

## Architecture

```
src/pyspark_sql_builder/
├── __init__.py     # exports: SparkSession, DataFrame, Column, GroupedData, functions, types
├── session.py      # SparkSession (+ Builder), entry point
├── dataframe.py    # DataFrame: query state machine, _build_sql(), generate_query(dialect)
├── column.py       # Column: wraps expression string in _expr, operator overloads, _to_expr() helper
├── group.py        # GroupedData: group_by().agg() chaining, lazy imports DataFrame to avoid circular dep
├── functions.py    # col, lit, count, when + WhenBuilder, 40+ SQL function constructors
├── readwriter.py   # DataFrameReader / DataFrameWriter stubs
└── types.py        # DataType, StringType, StructType, ArrayType, etc.
```

## Design rules

- **`generate_query(dialect=None)`** is the output method. Builds SQL string via `_build_sql()`, transpiles with `polyglot_sql.parse_one(sql).sql(dialect=target)`. Falls back to `transpile()`. Fast-paths "spark".
- **Immutability**: every DataFrame method returns `self._clone()` with new state. `_clone()` uses `__new__` + field copy.
- **Column stores `_expr`** (raw SQL fragment), not `_name`. `name` is a property that returns `_expr`.
- **`Column.__eq__` returns `Column`** (not `bool`), mimicking PySpark. Avoid using `==` in Python if-branches with Column; use `_expr` comparison instead.
- **`_to_expr(value)`** (in `column.py`) converts Python values to SQL literals: `str -> 'quoted'`, `None -> NULL`, `bool -> TRUE/FALSE`, `Column -> its _expr`.
- **`GroupedData` breaks circular import** via `TYPE_CHECKING` guard + lazy `from pyspark_sql_builder.dataframe import DataFrame as _DataFrame` inside `agg()`. Available as `df.groupBy(...)`.
- **camelCase API**: Methods mirror PySpark exactly: `groupBy`, `orderBy`, `selectExpr`, `withColumn`, `withColumnRenamed`, `unionAll`, `exceptAll`, `isNull`, `isNotNull`, `getOrCreate`. Functions shadow builtins: `sum`, `min`, `max`, `abs`, `round`.
- **polyglot-sql**: Python binding exposes Expression classes as read-only. Dict-based AST (`generate(dict)`) works but is too verbose for fluent construction. String + transpile is the right approach.

## Config

- Build: `uv_build` (not setuptools)
- Ruff: select `E,F,I,W,N,UP`, ignore `N802,N812` (N802: camelCase methods are PySpark convention; N812: functions imported as `F`)
- Type checker: pyrefly (not pyright)
- Tests: pytest, no DB, assert on `generate_query()` output
