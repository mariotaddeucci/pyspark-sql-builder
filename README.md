# pyspark-sql-builder

A PySpark SQL query builder that generates SQL for 32+ database dialects using [polyglot-sql](https://github.com/tobilg/polyglot) as its transpilation engine.

Write PySpark DataFrame code and generate dialect-specific SQL — no Spark cluster required.

## Why?

You know the PySpark DataFrame API but want to:

- Generate SQL for **DuckDB**, **Postgres**, **BigQuery**, **Snowflake**, or any of 32+ dialects
- Debug and share the SQL behind your DataFrame transformations
- Run PySpark-style pipelines on lightweight engines without a Spark cluster
- Build SQL programmatically with a familiar, well-documented API

## Installation

```bash
uv add pyspark-sql-builder
```

## Quick Start

```python
from pyspark_sql_builder import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()

df = (
    spark.table("orders")
    .join("customers", F.col("orders.customer_id") == F.col("customers.id"))
    .select("orders.id", "customers.name", "orders.amount")
    .where(F.col("orders.amount") > 100)
    .orderBy(F.col("orders.amount").desc())
    .limit(50)
)

# Generate Spark SQL (default dialect)
print(df.generate_query())

# Transpile to DuckDB, Postgres, BigQuery...
print(df.generate_query("duckdb"))
print(df.generate_query("postgres"))
print(df.generate_query("bigquery"))
```

## Example

```python
from pyspark_sql_builder import SparkSession, functions as F

spark = SparkSession(dialect="duckdb")

# Aggregation with filtering
result = (
    spark.table("sales")
    .select(F.col("category"), F.sum(F.col("amount")).alias("total"))
    .groupBy("category")
    .having(F.sum(F.col("amount")) > 1000)
    .orderBy(F.col("total").desc())
)

print(result.generate_query())
```

Output:

```sql
SELECT category, SUM(amount) AS total
FROM sales
GROUP BY category
HAVING SUM(amount) > 1000
ORDER BY total DESC
```

## API

The API mirrors PySpark's `DataFrame`, `Column`, and `functions` modules:

| PySpark | This project |
|---|---|
| `spark.table(...)` | `SparkSession.table(...)` |
| `df.select(...)` | `DataFrame.select(...)` |
| `df.where(...)` | `DataFrame.where(...)` |
| `df.join(...)` | `DataFrame.join(...)` |
| `df.groupBy(...)` | `DataFrame.groupBy(...)` |
| `df.orderBy(...)` | `DataFrame.orderBy(...)` |
| `df.agg(...)` | `DataFrame.agg(...)` |
| `F.col(...)` | `functions.col(...)` |
| `F.lit(...)` | `functions.lit(...)` |
| `F.count(...)` | `functions.count(...)` |

### `generate_query(dialect=None)`

The central method. Returns the SQL string for the given dialect. If `dialect` is `None`, uses the session's default dialect.

Supported dialects include: `spark`, `duckdb`, `postgres`, `bigquery`, `snowflake`, `mysql`, `sqlite`, `clickhouse`, `databricks`, `presto`, `trino`, and 20+ more.

## Development

```bash
# Setup
uv sync

# Run tests
uv run pytest

# Type check
uv run pyright

# Lint
uv run ruff check
```

## How it works

The builder constructs SQL strings from PySpark-style method calls. When `generate_query(dialect)` is called, if a dialect different from `spark` is requested, the SQL is transpiled via [polyglot-sql](https://pypi.org/project/polyglot-sql/) — a Rust-powered SQL transpiler supporting 32+ dialects.

## License

MIT
