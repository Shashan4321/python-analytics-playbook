"""The same KPI in pandas, Polars and DuckDB.

KPI: net revenue and order count per Indian fiscal year and category (returns excluded).
All three functions return an identical pandas DataFrame so results can be compared.
"""

from __future__ import annotations

import duckdb
import pandas as pd
import polars as pl

COLUMNS = ["fiscal_year", "category", "revenue", "orders"]


def _tidy(df: pd.DataFrame) -> pd.DataFrame:
    out = df[COLUMNS].copy()
    out["fiscal_year"] = out["fiscal_year"].astype("int64")
    out["category"] = out["category"].astype(str)
    out["orders"] = out["orders"].astype("int64")
    out["revenue"] = out["revenue"].astype("float64").round(2)
    return out.sort_values(["fiscal_year", "category"]).reset_index(drop=True)


def category_revenue_pandas(df: pd.DataFrame) -> pd.DataFrame:
    sales = df.loc[~df["returned"]]
    fy = sales["order_date"].dt.year + (sales["order_date"].dt.month >= 4).astype("int64")
    out = (
        sales.assign(fiscal_year=fy)
        .groupby(["fiscal_year", "category"], as_index=False, observed=True)
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    )
    return _tidy(out)


def category_revenue_polars(df: pd.DataFrame | pl.DataFrame) -> pd.DataFrame:
    lf = (df if isinstance(df, pl.DataFrame) else pl.from_pandas(df)).lazy()
    out = (
        lf.filter(~pl.col("returned"))
        .with_columns(
            fiscal_year=pl.col("order_date").dt.year() + (pl.col("order_date").dt.month() >= 4).cast(pl.Int32)
        )
        .group_by("fiscal_year", "category")
        .agg(revenue=pl.col("revenue").sum(), orders=pl.col("order_id").n_unique())
        .collect()
    )
    return _tidy(out.to_pandas())


SQL = """
SELECT
    year(order_date) + CASE WHEN month(order_date) >= 4 THEN 1 ELSE 0 END AS fiscal_year,
    category,
    SUM(revenue)             AS revenue,
    COUNT(DISTINCT order_id) AS orders
FROM sales
WHERE NOT returned
GROUP BY ALL
"""


def category_revenue_duckdb(
    source: pd.DataFrame | str, con: duckdb.DuckDBPyConnection | None = None
) -> pd.DataFrame:
    """Run the SQL over a pandas DataFrame, or over an existing DuckDB table when `source` is its name.

    Querying a DataFrame pays a conversion cost on every call; a DuckDB table (or Parquet files)
    is how the engine is used in a real warehouse.
    """
    own = con is None
    con = con or duckdb.connect()
    try:
        if isinstance(source, str):
            return _tidy(con.sql(SQL.replace("FROM sales", f"FROM {source}")).df())
        con.register("sales", source)
        try:
            return _tidy(con.sql(SQL).df())
        finally:
            con.unregister("sales")
    finally:
        if own:
            con.close()


ENGINES = {
    "pandas": category_revenue_pandas,
    "polars": category_revenue_polars,
    "duckdb": category_revenue_duckdb,
}
