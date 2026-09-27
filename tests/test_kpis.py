import pandas as pd
import pytest

from playbook.kpis import cohort_retention, monthly_revenue, net_sales, pareto, rfm, top_n_per_group


def test_net_sales_drops_returns(tiny):
    assert net_sales(tiny)["order_id"].tolist() == [1, 2, 4, 5]


def test_monthly_revenue_fills_gaps_and_growth(tiny):
    m = monthly_revenue(tiny)
    # Mar-2025 .. Apr-2026 = 14 months, including empty ones.
    assert len(m) == 14
    assert m.loc[m["month"] == pd.Period("2025-04", "M"), "revenue"].item() == 900.0  # return excluded
    apr26 = m.loc[m["month"] == pd.Period("2026-04", "M")].iloc[0]
    assert apr26["revenue"] == 1300.0
    assert apr26["yoy_pct"] == pytest.approx(1300 / 900 - 1)


def test_fytd_resets_every_april(tiny):
    m = monthly_revenue(tiny).set_index("month")
    assert m.loc[pd.Period("2025-03", "M"), "fytd_revenue"] == 1000.0  # last month of FY25
    assert m.loc[pd.Period("2025-04", "M"), "fytd_revenue"] == 900.0  # FY26 starts fresh


def test_top_n_per_group(sales):
    top = top_n_per_group(sales, "category", "product", n=2)
    assert top.groupby("category").size().eq(2).all()
    for _, grp in top.groupby("category"):
        assert grp["revenue"].is_monotonic_decreasing


def test_pareto_classes_are_ordered(sales):
    p = pareto(sales, "product")
    assert p["cum_share"].iloc[-1] == pytest.approx(1.0)
    assert list(dict.fromkeys(p["abc_class"])) == ["A", "B", "C"][: p["abc_class"].nunique()]
    assert p.loc[p["abc_class"] == "A", "revenue"].sum() / p["revenue"].sum() >= 0.80


def test_cohort_retention_starts_at_100_percent(sales):
    c = cohort_retention(sales)
    assert (c[0] == 1.0).all()
    assert ((c >= 0) & (c <= 1)).all().all()


def test_rfm_scores_and_segments(sales):
    r = rfm(sales)
    assert r["customer_id"].is_unique
    assert set(r[["r", "f", "m"]].stack().unique()) <= {1, 2, 3, 4, 5}
    # Most recent buyers get the best recency score.
    assert r.loc[r["recency_days"].idxmin(), "r"] == 5
    assert {"Champions", "Hibernating"} <= set(r["segment"])
