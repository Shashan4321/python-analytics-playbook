"""End-to-end example: generate data, validate, load, analyse and write the MIS workbook.

Usage:  python examples/generate_mis_report.py
Outputs: reports/MIS_Report.xlsx and reports/warehouse.duckdb
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from playbook.data import make_sales  # noqa: E402
from playbook.etl import EtlConfig, incremental_load  # noqa: E402
from playbook.kpis import monthly_revenue, pareto, rfm  # noqa: E402
from playbook.quality import flag_anomalies, validate  # noqa: E402
from playbook.reporting import build_mis_workbook, summary_table  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("mis")


def main() -> None:
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)

    raw = make_sales(n_orders=50_000, seed=42)
    checked = validate(raw)
    log.info(
        "Validation pass rate %.2f%% (%d rows quarantined)",
        checked.pass_rate * 100,
        len(checked.quarantined),
    )

    incremental_load(checked.valid, EtlConfig(warehouse=reports / "warehouse.duckdb"))

    monthly = monthly_revenue(checked.valid)
    spikes = monthly.loc[flag_anomalies(monthly["revenue"]), "month"].astype(str).tolist()
    abc = pareto(checked.valid, "product")["abc_class"].value_counts().to_dict()
    segments = rfm(checked.valid)["segment"].value_counts().to_dict()

    log.info("Anomalous months: %s", spikes or "none")
    log.info("Product ABC classes: %s", abc)
    log.info("Customer segments: %s", segments)
    print(summary_table(checked.valid).to_string(index=False))

    path = build_mis_workbook(checked.valid, reports / "MIS_Report.xlsx")
    log.info("MIS workbook written to %s", path)


if __name__ == "__main__":
    main()
