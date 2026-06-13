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
    .join("customers", ["customer_id"])
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

## Examples

### Aggregation with filtering

```python
spark = SparkSession(dialect="duckdb")
result = (
    spark.table("sales")
    .select(F.col("category"), F.sum(F.col("amount")).alias("total"))
    .groupBy("category")
    .having(F.sum(F.col("amount")) > 1000)
    .orderBy(F.col("total").desc())
)
print(result.generate_query())
```

```sql
SELECT category, SUM(amount) AS total
FROM sales
GROUP BY category
HAVING SUM(amount) > 1000
ORDER BY total DESC
```

### Window functions

```python
from pyspark_sql_builder import Window

w = Window.partitionBy("department").orderBy(F.col("salary").desc())
df = (
    spark.table("employees")
    .select(
        "name",
        "department",
        "salary",
        F.row_number().over(w).alias("rank"),
    )
)
print(df.generate_query())
```

### CASE / WHEN

```python
df = spark.table("orders").select(
    F.col("amount"),
    F.when(F.col("amount") > 100, "high")
     .when(F.col("amount") > 50, "medium")
     .otherwise("low")
     .alias("tier"),
)
print(df.generate_query())
```

### Join with USING

```python
df = spark.table("employees").join("departments", ["dept_id"])
print(df.generate_query())
# SELECT ... FROM employees JOIN departments USING (dept_id)
```

## API

The API mirrors PySpark's `DataFrame`, `Column`, `Window`, and `functions` modules:

| Category | PySpark | This project |
|---|---|---|
| Session | `spark.table(...)` | `SparkSession.table(...)` |
| Transformations | `df.select(...)` | `DataFrame.select(...)` |
| | `df.selectExpr(...)` | `DataFrame.selectExpr(...)` |
| | `df.where(...)` / `df.filter(...)` | `DataFrame.where(...)` / `filter(...)` |
| | `df.withColumn(...)` | `DataFrame.withColumn(...)` |
| | `df.withColumnRenamed(...)` | `DataFrame.withColumnRenamed(...)` |
| | `df.drop(...)` | `DataFrame.drop(...)` |
| | `df.distinct(...)` | `DataFrame.distinct(...)` |
| Joins | `df.join(other, on)` | `DataFrame.join(...)` |
| | `df.join(other, ["key"])` | `DataFrame.join(..., ["key"])` (USING) |
| Grouping | `df.groupBy(...)` | `DataFrame.groupBy(...)` |
| | `df.agg(...)` | `DataFrame.agg(...)` |
| | `df.having(...)` | `DataFrame.having(...)` |
| Ordering | `df.orderBy(...)` | `DataFrame.orderBy(...)` |
| Window | `Window.partitionBy(...)` | `Window.partitionBy(...)` |
| | `Window.partitionBy(...).orderBy(...)` | `Window.partitionBy(...).orderBy(...)` |
| Functions | `F.col(...)` | `functions.col(...)` |
| | `F.lit(...)` | `functions.lit(...)` |
| | `F.count(...)`, `F.sum(...)`, `F.avg(...)` | `functions.count/sum/avg/min/max(...)` |
| | `F.when(...).otherwise(...)` | `functions.when(...).otherwise(...)` |
| | `F.row_number()`, `F.rank()` | `functions.row_number/rank/dense_rank(...)` |
| | `F.lag(...)`, `F.lead(...)` | `functions.lag/lead(...)` |
| Output | `df.collect()` / `df.show()` | `df.generate_query(dialect)` |

### `generate_query(dialect=None)`

The central output method. Returns the SQL string for the given dialect. If `dialect` is `None`, uses the session's default dialect.

Supported dialects include: `spark`, `duckdb`, `postgres`, `bigquery`, `snowflake`, `mysql`, `sqlite`, `clickhouse`, `databricks`, `presto`, `trino`, and 20+ more.

## How it works

The builder constructs SQL strings from PySpark-style method calls. All identifiers are auto-quoted with backticks to handle reserved words and special characters. When `generate_query(dialect)` is called, if a dialect different from `spark` is requested, the SQL is transpiled via [polyglot-sql](https://pypi.org/project/polyglot-sql/) — a Rust-powered SQL transpiler supporting 32+ dialects.

## Development

```bash
# Setup
uv sync

# Install git hooks (ruff fix → ruff format → pyrefly check)
prek install

# Run all checks
prek run --all-files

# Run tests
uv run pytest

# Type check
uv run pyrefly check src/

# Lint & format
uv run ruff check
uv run ruff format
```

## License

MIT
