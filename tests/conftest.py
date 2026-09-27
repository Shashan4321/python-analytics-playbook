import pandas as pd
import pytest

from playbook.data import make_sales


@pytest.fixture(scope="session")
def sales() -> pd.DataFrame:
    return make_sales(n_orders=20_000, seed=7)


@pytest.fixture
def tiny() -> pd.DataFrame:
    """Hand-made rows where every expected number can be checked by eye."""
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5],
            "order_date": pd.to_datetime(
                ["2025-03-15", "2025-04-10", "2025-04-20", "2026-04-05", "2026-04-06"]
            ),
            "customer_id": ["C00001", "C00001", "C00002", "C00002", "C00003"],
            "region": ["North", "South", "North", "East", "West"],
            "category": ["Home", "Home", "Grocery", "Home", "Grocery"],
            "product": ["Lamp", "Rug", "Tea", "Lamp", "Rice"],
            "quantity": [1, 2, 1, 1, 3],
            "unit_price": [1000.0, 500.0, 200.0, 1000.0, 100.0],
            "discount": [0.0, 0.10, 0.0, 0.0, 0.0],
            "returned": [False, False, True, False, False],
            "revenue": [1000.0, 900.0, 200.0, 1000.0, 300.0],
        }
    )
