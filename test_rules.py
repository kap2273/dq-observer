import pandas as pd
from rule import check_rules


def make_orders():
    """A small clean table. Each test copies it and breaks one thing."""
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [10, 20, 30],
        "amount": [5.0, 10.0, 15.0],
        "status": ["placed", "shipped", "cancelled"],
    })


def test_clean_data_passes():
    df = make_orders()
    assert check_rules(df) == []


def test_duplicate_order_id():
    df = make_orders()
    df.loc[2, "order_id"] = 1          # row 3 now repeats order 1
    assert "Duplicate order_id found" in check_rules(df)


def test_blank_customer():
    df = make_orders()
    df.loc[0, "customer_id"] = None
    assert "Null customer_id found" in check_rules(df)


def test_negative_amount():
    df = make_orders()
    df.loc[1, "amount"] = -5.0
    assert "Negative amount found" in check_rules(df)


def test_invalid_status():
    df = make_orders()
    df.loc[0, "status"] = "lost"
    assert "Invalid status found" in check_rules(df)
    