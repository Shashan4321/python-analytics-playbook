"""Seeded synthetic retail sales data.

Everything here is generated from a fixed seed. No real, employer or client data is used.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CATALOG: dict[str, dict[str, float]] = {
    "Electronics": {"Laptop": 62000, "Mobile": 24000, "Headphones": 3500, "Monitor": 14000},
    "Home": {"Mattress": 18000, "Curtains": 4200, "Rug": 6500, "Lamp": 2200},
    "Fashion": {"Shirt": 1500, "Saree": 5200, "Sneakers": 4800, "Watch": 7900},
    "Grocery": {"Tea": 450, "Rice": 900, "Snacks": 250, "Oil": 1100},
}
REGIONS = ("North", "South", "East", "West")
DISCOUNTS = (0.0, 0.05, 0.10, 0.20)


def make_sales(
    n_orders: int = 50_000,
    start: str = "2023-04-01",
    end: str = "2026-03-31",
    seed: int = 42,
) -> pd.DataFrame:
    """Return one row per order line with a festive-season peak and steady growth.

    Columns: order_id, order_date, customer_id, region, category, product, quantity,
    unit_price, discount, returned, revenue (net of discount, gross of returns).
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, end, freq="D")

    # Oct-Nov (Diwali season) is busier, and the business grows ~40% over the period.
    festive = np.where(dates.month.isin([10, 11]), 1.8, 1.0)
    growth = np.linspace(1.0, 1.4, len(dates))
    weights = festive * growth
    order_dates = rng.choice(dates.to_numpy(), size=n_orders, p=weights / weights.sum())

    products = [(cat, prod, price) for cat, items in CATALOG.items() for prod, price in items.items()]
    pick = rng.integers(0, len(products), n_orders)
    category = np.array([products[i][0] for i in pick])
    product = np.array([products[i][1] for i in pick])
    base_price = np.array([products[i][2] for i in pick])

    n_customers = max(n_orders // 8, 1)
    customer_num = rng.integers(1, n_customers + 1, n_orders)

    quantity = rng.integers(1, 5, n_orders)
    unit_price = (base_price * rng.uniform(0.9, 1.1, n_orders)).round(2)
    discount = rng.choice(DISCOUNTS, size=n_orders, p=[0.5, 0.25, 0.15, 0.10])
    returned = rng.random(n_orders) < 0.04

    df = pd.DataFrame(
        {
            "order_date": pd.to_datetime(order_dates),
            "customer_id": [f"C{n:05d}" for n in customer_num],
            "region": rng.choice(REGIONS, size=n_orders),
            "category": category,
            "product": product,
            "quantity": quantity.astype("int64"),
            "unit_price": unit_price,
            "discount": discount,
            "returned": returned,
        }
    )
    df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
    df = df.sort_values("order_date", kind="stable").reset_index(drop=True)
    df.insert(0, "order_id", np.arange(1, n_orders + 1, dtype="int64"))
    return df
