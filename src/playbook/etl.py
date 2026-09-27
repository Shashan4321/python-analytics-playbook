"""Production-style ETL: config, logging, idempotent upserts and partitioned Parquet."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import duckdb
import pandas as pd

from playbook.fiscal import fiscal_year

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class EtlConfig:
    warehouse: Path
    table: str = "fact_sales"
    key: str = "order_id"


@dataclass(frozen=True)
class LoadResult:
    inserted: int
    updated: int
    total_rows: int
    watermark: pd.Timestamp | None


def incremental_load(batch: pd.DataFrame, config: EtlConfig) -> LoadResult:
    """Upsert a batch into DuckDB by key inside one transaction.

    Re-running the same batch changes nothing (idempotent): rows are replaced, not duplicated.
    Duplicate keys inside the batch keep the last occurrence.
    """
    batch = batch.drop_duplicates(subset=config.key, keep="last")
    table, key = config.table, config.key

    with duckdb.connect(str(config.warehouse)) as con:
        con.register("batch", batch)
        con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM batch WHERE false")

        existing = con.execute(
            f"SELECT COUNT(*) FROM batch WHERE {key} IN (SELECT {key} FROM {table})"
        ).fetchone()[0]

        con.execute("BEGIN TRANSACTION")
        try:
            con.execute(f"DELETE FROM {table} WHERE {key} IN (SELECT {key} FROM batch)")
            con.execute(f"INSERT INTO {table} SELECT * FROM batch")
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            log.exception("Load into %s failed, transaction rolled back", table)
            raise

        total, watermark = con.execute(f"SELECT COUNT(*), MAX(order_date) FROM {table}").fetchone()
        con.unregister("batch")

    result = LoadResult(
        inserted=len(batch) - existing,
        updated=existing,
        total_rows=total,
        watermark=pd.Timestamp(watermark) if watermark is not None else None,
    )
    log.info(
        "Loaded %s: %d inserted, %d updated, %d total, watermark %s",
        table,
        result.inserted,
        result.updated,
        result.total_rows,
        result.watermark,
    )
    return result


def write_partitioned_parquet(df: pd.DataFrame, out_dir: Path) -> list[Path]:
    """Write one Parquet folder per fiscal year (fiscal_year=2026/...), the lakehouse layout."""
    out = df.assign(fiscal_year=fiscal_year(df["order_date"]))
    out.to_parquet(out_dir, partition_cols=["fiscal_year"], index=False)
    return sorted(p for p in Path(out_dir).iterdir() if p.is_dir())
