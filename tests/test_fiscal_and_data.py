import pandas as pd

from playbook.data import make_sales
from playbook.fiscal import date_dim, fiscal_month, fiscal_quarter, fiscal_year, fy_label


def test_fiscal_year_boundaries():
    d = pd.Series(pd.to_datetime(["2025-03-31", "2025-04-01", "2026-03-31", "2026-04-01"]))
    assert fiscal_year(d).tolist() == [2025, 2026, 2026, 2027]


def test_fiscal_quarter_and_month():
    d = pd.Series(pd.to_datetime(["2025-04-01", "2025-07-01", "2025-12-31", "2026-03-01"]))
    assert fiscal_quarter(d).tolist() == [1, 2, 3, 4]
    assert fiscal_month(d).tolist() == [1, 4, 9, 12]


def test_fy_labels():
    assert fy_label(2026) == "FY26"
    assert fy_label(2026, long=True) == "FY2025-26"
    assert fy_label(pd.Series([2025, 2026])).tolist() == ["FY25", "FY26"]


def test_date_dim_covers_every_day():
    dim = date_dim("2024-04-01", "2025-03-31")
    assert len(dim) == 365
    assert dim["fiscal_year"].unique().tolist() == [2025]
    assert dim["date"].is_unique


def test_make_sales_is_reproducible_and_consistent():
    a, b = make_sales(1_000, seed=1), make_sales(1_000, seed=1)
    pd.testing.assert_frame_equal(a, b)
    assert a["order_id"].is_unique and a["order_date"].is_monotonic_increasing
    expected = (a["quantity"] * a["unit_price"] * (1 - a["discount"])).round(2)
    pd.testing.assert_series_equal(a["revenue"], expected, check_names=False)


def test_festive_months_are_busier():
    df = make_sales(30_000, seed=3)
    by_month = df.groupby(df["order_date"].dt.month).size()
    assert by_month.loc[[10, 11]].mean() > 1.4 * by_month.loc[[6, 7]].mean()
