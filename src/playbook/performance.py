"""Pandas performance patterns: memory-efficient dtypes and vectorisation."""

from __future__ import annotations

import numpy as np
import pandas as pd


def memory_mb(df: pd.DataFrame) -> float:
    """True memory footprint in MB, including string contents."""
    return df.memory_usage(deep=True).sum() / 1024**2


def optimize_dtypes(df: pd.DataFrame, category_ratio: float = 0.5) -> pd.DataFrame:
    """Downcast numbers and turn low-cardinality text into categoricals.

    A text column becomes categorical when unique values / rows < category_ratio.
    Values are unchanged; only the storage type shrinks.
    """
    out = df.copy()
    for col in out.columns:
        s = out[col]
        if pd.api.types.is_bool_dtype(s) or pd.api.types.is_datetime64_any_dtype(s):
            continue
        if pd.api.types.is_integer_dtype(s):
            out[col] = pd.to_numeric(s, downcast="integer")
        elif pd.api.types.is_float_dtype(s):
            # float32 keeps ~7 significant digits: fine for prices, not for ledger totals.
            out[col] = pd.to_numeric(s, downcast="float")
        elif (pd.api.types.is_object_dtype(s) or pd.api.types.is_string_dtype(s)) and (
            s.nunique(dropna=False) / max(len(s), 1) < category_ratio
        ):
            out[col] = s.astype("category")
    return out


def revenue_loop(df: pd.DataFrame) -> pd.Series:
    """Row-by-row version. Shown only to benchmark against the vectorised one."""
    values = [
        round(row.quantity * row.unit_price * (1 - row.discount), 2) for row in df.itertuples(index=False)
    ]
    return pd.Series(values, index=df.index, name="revenue")


def revenue_vectorized(df: pd.DataFrame) -> pd.Series:
    """Whole-column arithmetic: one pass in compiled code."""
    return (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2).rename("revenue")


def discount_band_apply(df: pd.DataFrame) -> pd.Series:
    """Slow pattern: a Python function per row via .apply(axis=1), reading two columns.

    Deep = 20%+ off, or 10%+ off on a bulk order (3+ units). Light = any other discount.
    """

    def band(row: pd.Series) -> str:
        if row["discount"] >= 0.20 or (row["discount"] >= 0.10 and row["quantity"] >= 3):
            return "Deep"
        if row["discount"] > 0:
            return "Light"
        return "Full price"

    return df.apply(band, axis=1)


def discount_band_select(df: pd.DataFrame) -> pd.Series:
    """Fast pattern: the same rules as boolean masks and one np.select."""
    d, q = df["discount"], df["quantity"]
    deep = (d >= 0.20) | ((d >= 0.10) & (q >= 3))
    return pd.Series(
        np.select([deep, d > 0], ["Deep", "Light"], default="Full price"),
        index=df.index,
    )
