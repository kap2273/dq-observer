import pandas as pd
from profile_batch import profile


def test_profile_metrics(tmp_path):
    # 4 orders: order 3 is duplicated, one customer is blank, one is cancelled
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 3],
        "customer_id": [10, None, 30, 40],
        "status": ["placed", "shipped", "cancelled", "placed"],
        "amount": [10.0, 20.0, 30.0, 40.0],
    })
    path = tmp_path / "orders.csv"
    df.to_csv(path, index=False)

    m = profile(path)

    assert m["row_count"] == 4
    assert m["duplicate_rate"] == 0.25      # 1 of 4 ids is a repeat
    assert m["cancelled_rate"] == 0.25      # 1 of 4 is cancelled
    assert m["amount_mean"] == 25.0         # (10+20+30+40) / 4
    assert m["null_rate"] == 0.0625         # 1 blank out of 16 cells