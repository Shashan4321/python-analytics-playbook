# Python Analytics Playbook

[![CI](https://github.com/Shashan4321/python-analytics-playbook/actions/workflows/ci.yml/badge.svg)](https://github.com/Shashan4321/python-analytics-playbook/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2%2B%20%2F%203.0-150458?logo=pandas)
![Polars](https://img.shields.io/badge/Polars-1.x-CD792C)
![DuckDB](https://img.shields.io/badge/DuckDB-1.x-FFF000?logo=duckdb&logoColor=black)
![License](https://img.shields.io/badge/license-MIT-green)

**Tested, reusable Python patterns for business analytics:** the code I reach for when turning raw
sales, finance and operations data into KPIs, clean tables and MIS reports.

Every pattern is a small function with a test, not a notebook cell. Numbers in this README come from
running the code in this repo (`benchmarks/RESULTS.md`), not from estimates.

| # | Module | What it covers | Why it matters in a real team |
|---|---|---|---|
| 1 | [`performance.py`](src/playbook/performance.py) | Memory-efficient dtypes, vectorisation vs loops and `.apply(axis=1)` | Laptops and Power BI gateways run out of RAM long before they run out of CPU |
| 2 | [`engines.py`](src/playbook/engines.py) | The same KPI in **pandas, Polars and DuckDB**, proven identical | Choosing the right engine for the job instead of defaulting to pandas |
| 3 | [`kpis.py`](src/playbook/kpis.py) + [`fiscal.py`](src/playbook/fiscal.py) | Indian FY calendar, MoM / YoY / FYTD, Top-N per group, Pareto ABC, cohort retention, RFM segments | KPIs defined the way finance defines them (returns excluded, April-March year) |
| 4 | [`quality.py`](src/playbook/quality.py) | Pandera schema with cross-column business rules, quarantine of bad rows, source-vs-target reconciliation, robust anomaly flags | Bad rows are isolated and reported instead of silently breaking a dashboard |
| 5 | [`etl.py`](src/playbook/etl.py) | Config dataclass, logging, **idempotent** transactional upserts into DuckDB, partitioned Parquet | Re-running a failed job must never double-count revenue |
| 6 | [`reporting.py`](src/playbook/reporting.py) | Formatted Excel MIS workbook: Indian ₹ lakh/crore number format, YoY heatmap, frozen headers | The monthly report finance actually opens, generated in seconds |

## Results (1,000,000 order lines)

Measured with `python benchmarks/run_benchmarks.py` on a Windows 11 laptop (Python 3.12, pandas 3.0,
Polars 1.44, DuckDB 1.5). Your timings will differ; the ratios are the point.

**Memory:** `optimize_dtypes` cut a 1M-row sales table from **100.3 MB to 40.8 MB (-59%)** with no values changed.

| Vectorisation (200k rows) | Slow pattern | Fast pattern | Speed-up |
|---|---:|---:|---:|
| Line revenue | `itertuples` loop: 1.95 s | column maths: 4.7 ms | **415x** |
| Discount band, 2-column rule | `.apply(axis=1)`: 2.41 s | `np.select`: 63.6 ms | **38x** |

| Same KPI, three engines | Time |
|---|---:|
| DuckDB, native table | **118 ms** |
| Polars, lazy | 141 ms |
| pandas | 788 ms |
| DuckDB querying a pandas DataFrame | 2.21 s |

The last row is deliberate: querying a DataFrame converts it on every call. Load once into a table
(1.7 s here) or read Parquet, then query. That is how DuckDB is used in a warehouse.

## Quick start

```bash
git clone https://github.com/Shashan4321/python-analytics-playbook.git
cd python-analytics-playbook
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements-dev.txt

pytest                            # 31 tests, about 5 seconds
python examples/generate_mis_report.py   # validate -> load -> KPIs -> reports/MIS_Report.xlsx
python benchmarks/run_benchmarks.py      # rewrites benchmarks/RESULTS.md on your machine
```

## Examples

```python
from playbook.data import make_sales
from playbook.kpis import monthly_revenue, pareto, rfm
from playbook.quality import validate
from playbook.etl import EtlConfig, incremental_load

sales = make_sales(n_orders=50_000)  # seeded synthetic data

checked = validate(sales)  # every rule at once, bad rows quarantined
print(f"pass rate {checked.pass_rate:.1%}")

incremental_load(checked.valid, EtlConfig(warehouse="warehouse.duckdb"))  # safe to re-run

monthly_revenue(checked.valid)[["month", "revenue", "mom_pct", "yoy_pct", "fytd_revenue"]]
pareto(checked.valid, "product")  # A / B / C classes
rfm(checked.valid)["segment"].value_counts()  # Champions, Loyal, At Risk, ...
```

## Design decisions

| Decision | Why |
|---|---|
| Functions + tests, not notebooks | Reusable in scheduled jobs and reviewable in a pull request. Notebooks are for exploring, not for code other people depend on. |
| Net revenue excludes returns everywhere | One definition of "revenue", so Python output matches the finance dashboard. |
| Indian FY labelled by the year it ends (`FY26` = Apr 2025 to Mar 2026) | Matches how Indian finance teams and statutory reports label the year. |
| Pandera with `lazy=True` + quarantine | See all problems in one run, and keep loading the good rows instead of failing the whole batch. |
| Robust z-score (median/MAD) for anomalies | A single spike cannot inflate the standard deviation and hide itself. On this seasonal data it flags the Oct-Nov festive peaks, which is correct: in production you would de-seasonalise first, or compare with the same month last year. |
| Delete-then-insert inside one transaction for upserts | Idempotent and simple; a failure rolls back so the table is never half-loaded. |
| `float32` only where precision allows | Fine for unit prices; ledger totals stay `float64` (or decimals in the warehouse). |

## Project structure

```
src/playbook/
  data.py          seeded synthetic retail data (no real or employer data)
  fiscal.py        Indian financial-year calendar and date dimension
  kpis.py          MoM / YoY / FYTD, Top-N, Pareto, cohorts, RFM
  performance.py   dtype optimisation, vectorised vs slow patterns
  engines.py       pandas vs Polars vs DuckDB, same KPI
  quality.py       Pandera schema, quarantine, reconciliation, anomalies
  etl.py           idempotent DuckDB upserts, partitioned Parquet
  reporting.py     formatted Excel MIS workbook
tests/             31 pytest tests (hand-checkable fixtures + 20k-row data)
benchmarks/        run_benchmarks.py and RESULTS.md
examples/          generate_mis_report.py (end to end)
.github/workflows/ ci.yml (ruff + pytest on 3.11 / 3.12), monthly-mis.yml (scheduled report)
```

## Automation

[`monthly-mis.yml`](.github/workflows/monthly-mis.yml) runs on the 1st of every month (and on demand):
it validates the data, loads the warehouse, builds `MIS_Report.xlsx` and attaches it to the run as a
downloadable artifact. The same job at work would read from the ERP/warehouse and e-mail the file.

## Data and licence

All data is synthetic, generated by `make_sales()` from a fixed seed. No employer or client data,
schema or code is used. Code is released under the MIT License.

## Author

**Shashank Singh**, Senior Data Analyst (Power BI · Microsoft Fabric · Snowflake · SQL · Python · GenAI)
[Portfolio](https://shashan4321.github.io) · [LinkedIn](https://linkedin.com/in/shashank-moon) · [GitHub](https://github.com/Shashan4321)

*Professional impact:* processed 500K+ row datasets with Pandas and NumPy, improved data accuracy by 30%
with automated validation, and automated 15+ weekly and monthly MIS reports (10+ hours saved per week).
This repo shows the same techniques on public-safe synthetic data.
