import pandas as pd
import polars as pl
import pytest

from playbook.engines import ENGINES, category_revenue_polars
from playbook.performance import (
    discount_band_apply,
    discount_band_select,
    memory_mb,
    optimize_dtypes,
    revenue_loop,
    revenue_vectorized,
)


def test_optimize_dtypes_shrinks_memory_without_changing_values(sales):
    small = optimize_dtypes(sales)
    assert memory_mb(small) < memory_mb(sales) * 0.6
    assert isinstance(small["category"].dtype, pd.CategoricalDtype)
    assert small["order_id"].dtype.itemsize < 8
    assert small["category"].astype(str).tolist() == sales["category"].astype(str).tolist()
    assert (small["unit_price"].astype("float64") - sales["unit_price"]).abs().max() < 0.01


def test_vectorized_matches_loop(sales):
    head = sales.head(2_000)
    pd.testing.assert_series_equal(revenue_loop(head), revenue_vectorized(head))


def test_select_matches_apply(sales):
    assert discount_band_select(sales).tolist() == discount_band_apply(sales).tolist()


def test_all_engines_agree(sales):
    results = {name: fn(sales) for name, fn in ENGINES.items()}
    base = results["pandas"]
    assert len(base) == base["fiscal_year"].nunique() * base["category"].nunique()
    for name, result in results.items():
        pd.testing.assert_frame_equal(result, base, check_exact=False, rtol=1e-9, obj=name)


def test_duckdb_native_table_matches_dataframe_query(sales):
    import duckdb

    with duckdb.connect() as con:
        con.execute("CREATE TABLE sales_tbl AS SELECT * FROM sales")
        from_table = ENGINES["duckdb"]("sales_tbl", con)
    pd.testing.assert_frame_equal(from_table, ENGINES["pandas"](sales))


def test_polars_accepts_native_frame(sales):
    native = pl.from_pandas(sales)
    pd.testing.assert_frame_equal(category_revenue_polars(native), ENGINES["pandas"](sales))


@pytest.mark.parametrize("name", list(ENGINES))
def test_engines_exclude_returns(tiny, name):
    out = ENGINES[name](tiny)
    grocery_fy26 = out.query("fiscal_year == 2026 and category == 'Grocery'")
    assert grocery_fy26.empty  # the only FY26 grocery line was returned
