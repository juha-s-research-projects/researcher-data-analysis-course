# Storage benchmark

Generates the chart in the Storage chapter (`course/docs/assets/storage-benchmark.png`).

One realistic question — a filtered group-by aggregation —

```sql
SELECT category, COUNT(*), AVG(value), SUM(amount)
FROM data WHERE amount > 100 GROUP BY category
```

is answered against the same synthetic data held four ways, across 1k → 10M rows:
CSV + polars, Parquet + polars, Excel, and SQLite.

## Run

```bash
uv run benchmark.py                 # full sweep (first run pulls wheels)
BENCH_ROWS=1000,10000 uv run benchmark.py   # quick smoke test
```

## What is (and isn't) being measured

- **File formats (CSV, Parquet, Excel) are re-read on every query** — the reality
  of a pile of files. polars scans lazily (projection + predicate pushdown).
- **SQLite is loaded once (untimed), then queried** — the entire reason to use a
  store. It gets a covering index on `(category, amount, value)` — the columns the
  query touches — so the row store is not handicapped against columnar Parquet.
- **Excel** is marked DNF beyond its hard 1,048,576-row limit.

Outputs: `results.json` (raw medians) and the PNG. The `_work/` scratch dir holds
the generated artifacts and can be deleted.
