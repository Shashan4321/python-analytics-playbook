"""Indian financial-year calendar (April to March) helpers.

Convention: FY26 = 1 Apr 2025 to 31 Mar 2026, labelled by the year it ends in.
"""

from __future__ import annotations

import pandas as pd

FY_START_MONTH = 4


def fiscal_year(dates: pd.Series, start_month: int = FY_START_MONTH) -> pd.Series:
    """Fiscal year number, e.g. 2026 for any date from Apr 2025 to Mar 2026."""
    d = pd.to_datetime(dates)
    return (d.dt.year + (d.dt.month >= start_month).astype("int64")).astype("int64")


def fiscal_quarter(dates: pd.Series, start_month: int = FY_START_MONTH) -> pd.Series:
    """Fiscal quarter 1-4, where Q1 = Apr-Jun for an April start."""
    d = pd.to_datetime(dates)
    return (((d.dt.month - start_month) % 12) // 3 + 1).astype("int64")


def fiscal_month(dates: pd.Series, start_month: int = FY_START_MONTH) -> pd.Series:
    """Month number inside the fiscal year, 1 = April."""
    d = pd.to_datetime(dates)
    return ((d.dt.month - start_month) % 12 + 1).astype("int64")


def fy_label(fy: int | pd.Series, long: bool = False) -> str | pd.Series:
    """'FY26', or 'FY2025-26' when long=True."""
    if isinstance(fy, pd.Series):
        return fy.map(lambda y: fy_label(int(y), long))
    return f"FY{fy - 1}-{str(fy)[-2:]}" if long else f"FY{str(fy)[-2:]}"


def date_dim(start: str, end: str, start_month: int = FY_START_MONTH) -> pd.DataFrame:
    """A date dimension table, the same shape a Power BI calendar table would have."""
    dates = pd.Series(pd.date_range(start, end, freq="D"), name="date")
    return pd.DataFrame(
        {
            "date": dates,
            "year": dates.dt.year,
            "month": dates.dt.month,
            "month_name": dates.dt.strftime("%b"),
            "fiscal_year": fiscal_year(dates, start_month),
            "fiscal_quarter": fiscal_quarter(dates, start_month),
            "fiscal_month": fiscal_month(dates, start_month),
            "is_weekend": dates.dt.dayofweek >= 5,
        }
    )
