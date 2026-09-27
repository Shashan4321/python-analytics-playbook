"""Business KPIs written the way finance defines them.

Net revenue excludes returned lines. Every function takes the order-line table from
`playbook.data.make_sales` (or any table with the same columns) and returns a new frame.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from playbook.fiscal import fiscal_year


def net_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Order lines that count towards revenue (returns removed)."""
    return df.loc[~df["returned"]]


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Net revenue per calendar month, with empty months filled as 0.

    Adds MoM %, YoY % and fiscal-year-to-date revenue.
    """
    sales = net_sales(df)
    month = sales["order_date"].dt.to_period("M")
    out = sales.groupby(month)["revenue"].sum()

    full = pd.period_range(out.index.min(), out.index.max(), freq="M")
    out = out.reindex(full, fill_value=0.0).rename_axis("month").reset_index()
    out["month_start"] = out["month"].dt.to_timestamp()
    out["fiscal_year"] = fiscal_year(out["month_start"])

    out["mom_pct"] = out["revenue"].pct_change(1)
    out["yoy_pct"] = out["revenue"].pct_change(12)
    out["fytd_revenue"] = out.groupby("fiscal_year")["revenue"].cumsum()
    return out


def top_n_per_group(
    df: pd.DataFrame, group: str, item: str, value: str = "revenue", n: int = 3
) -> pd.DataFrame:
    """Top n items inside each group, like RANKX / ROW_NUMBER() OVER (PARTITION BY ...)."""
    totals = df.groupby([group, item], as_index=False, observed=True)[value].sum()
    totals["rank"] = (
        totals.groupby(group, observed=True)[value].rank(method="first", ascending=False).astype(int)
    )
    return totals.loc[totals["rank"] <= n].sort_values([group, "rank"]).reset_index(drop=True)


def pareto(df: pd.DataFrame, item: str, value: str = "revenue") -> pd.DataFrame:
    """ABC classification: A = items making up the first 80% of value, B = next 15%, C = rest."""
    totals = df.groupby(item, observed=True)[value].sum().sort_values(ascending=False).reset_index()
    share = totals[value] / totals[value].sum()
    totals["cum_share"] = share.cumsum()
    # An item is class A if the running share *before* it was still under 80%.
    before = totals["cum_share"] - share
    totals["abc_class"] = np.select([before < 0.80, before < 0.95], ["A", "B"], default="C")
    return totals


def cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Share of each monthly acquisition cohort still buying N months later.

    Rows are cohorts (first purchase month), columns are months since first purchase.
    """
    sales = net_sales(df)[["customer_id", "order_date"]].copy()
    sales["order_month"] = sales["order_date"].dt.to_period("M")
    sales["cohort"] = sales.groupby("customer_id")["order_month"].transform("min")
    sales["period"] = (sales["order_month"] - sales["cohort"]).map(lambda offset: offset.n)

    active = sales.groupby(["cohort", "period"])["customer_id"].nunique().unstack(fill_value=0)
    return active.div(active[0], axis=0)


def rfm(df: pd.DataFrame, as_of: pd.Timestamp | None = None) -> pd.DataFrame:
    """Recency, frequency, monetary scores (1-5) and a named segment per customer."""
    sales = net_sales(df)
    as_of = as_of or sales["order_date"].max() + pd.Timedelta(days=1)

    table = sales.groupby("customer_id").agg(
        last_order=("order_date", "max"),
        frequency=("order_id", "nunique"),
        monetary=("revenue", "sum"),
    )
    table["recency_days"] = (as_of - table["last_order"]).dt.days

    def score(s: pd.Series, reverse: bool = False) -> pd.Series:
        # Rank first so ties never produce duplicate bin edges.
        ranked = s.rank(method="first", ascending=not reverse)
        return pd.qcut(ranked, 5, labels=[1, 2, 3, 4, 5]).astype(int)

    table["r"] = score(table["recency_days"], reverse=True)
    table["f"] = score(table["frequency"])
    table["m"] = score(table["monetary"])

    r, f = table["r"], table["f"]
    table["segment"] = np.select(
        [(r >= 4) & (f >= 4), f >= 4, (r <= 2) & (f >= 3), (r >= 4) & (f <= 2), (r <= 2) & (f <= 2)],
        ["Champions", "Loyal", "At Risk", "New", "Hibernating"],
        default="Needs Attention",
    )
    return table.drop(columns="last_order").reset_index()
