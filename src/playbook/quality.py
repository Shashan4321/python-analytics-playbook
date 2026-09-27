"""Data quality: schema validation with quarantine, reconciliation and anomaly flags."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import pandera.pandas as pa

from playbook.data import CATALOG, REGIONS

SALES_SCHEMA = pa.DataFrameSchema(
    {
        "order_id": pa.Column("int64", pa.Check.gt(0), unique=True),
        "order_date": pa.Column("datetime64[ns]"),
        "customer_id": pa.Column(str, pa.Check.str_matches(r"^C\d{5}$")),
        "region": pa.Column(str, pa.Check.isin(REGIONS)),
        "category": pa.Column(str, pa.Check.isin(list(CATALOG))),
        "quantity": pa.Column("int64", pa.Check.in_range(1, 100)),
        "unit_price": pa.Column(float, pa.Check.gt(0)),
        "discount": pa.Column(float, pa.Check.in_range(0, 0.5)),
        "returned": pa.Column(bool),
        "revenue": pa.Column(float, pa.Check.ge(0)),
    },
    checks=[
        # Business rule across columns: revenue must equal qty x price x (1 - discount).
        pa.Check(
            lambda d: pd.Series(
                np.isclose(d["revenue"], d["quantity"] * d["unit_price"] * (1 - d["discount"]), atol=0.01),
                index=d.index,
            ),
            error="revenue does not match quantity x unit_price x (1 - discount)",
        )
    ],
    coerce=True,
)


@dataclass
class ValidationResult:
    valid: pd.DataFrame
    quarantined: pd.DataFrame
    failures: pd.DataFrame

    @property
    def pass_rate(self) -> float:
        total = len(self.valid) + len(self.quarantined)
        return len(self.valid) / total if total else 1.0


def validate(df: pd.DataFrame, schema: pa.DataFrameSchema = SALES_SCHEMA) -> ValidationResult:
    """Validate every rule at once (lazy) and quarantine bad rows instead of failing the load."""
    try:
        valid = schema.validate(df, lazy=True)
        return ValidationResult(valid, df.iloc[0:0], pd.DataFrame())
    except pa.errors.SchemaErrors as exc:
        failures = exc.failure_cases
        bad_index = failures["index"].dropna().unique()
        quarantined = df.loc[df.index.isin(bad_index)]
        # Re-validate the clean part so the returned frame has coerced dtypes.
        valid = schema.validate(df.loc[~df.index.isin(bad_index)], lazy=True)
        return ValidationResult(valid, quarantined, failures)


def reconcile(
    source: pd.DataFrame,
    target: pd.DataFrame,
    key: str,
    amount_cols: list[str],
    tolerance: float = 0.01,
) -> pd.DataFrame:
    """Source-vs-target checks used after a migration or load. One row per check."""
    src_keys, tgt_keys = set(source[key]), set(target[key])
    dupes = int(target[key].duplicated().sum())
    checks = [
        ("row_count", len(source), len(target), len(source) == len(target)),
        ("missing_in_target", len(src_keys - tgt_keys), 0, not (src_keys - tgt_keys)),
        ("unexpected_in_target", len(tgt_keys - src_keys), 0, not (tgt_keys - src_keys)),
        ("duplicate_keys_in_target", dupes, 0, dupes == 0),
    ]
    for col in amount_cols:
        s, t = round(float(source[col].sum()), 2), round(float(target[col].sum()), 2)
        checks.append((f"sum_{col}", s, t, abs(s - t) <= tolerance))
    return pd.DataFrame(checks, columns=["check", "source", "target", "passed"])


def flag_anomalies(values: pd.Series, threshold: float = 3.5) -> pd.Series:
    """Robust z-score (median / MAD). Unlike mean/std, one spike cannot hide itself."""
    median = values.median()
    mad = (values - median).abs().median()
    if mad == 0:
        return pd.Series(False, index=values.index)
    robust_z = 0.6745 * (values - median) / mad
    return robust_z.abs() > threshold
