import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
def profile(path):
    df = pd.read_csv(path)
    metrics = {
        "file": path.name,
        "row_count": len(df),
        "null_rate": round(df.isna().mean().mean(), 4),
        "duplicate_rate": round(df["order_id"].duplicated().mean(), 4),
        "amount_mean": round(df["amount"].mean(), 4),
        "amount_min": df["amount"].min(),
        "amount_max": df["amount"].max(),
        "cancelled_rate": round((df["status"] == "cancelled").mean(), 4),
    }
    return metrics
if __name__ == "__main__":
    results = []
    files = sorted(Path("data/batches").glob("orders_*.csv"))
    for f in files:
        result = profile(f)
        results.append(result)

    table = pd.DataFrame(results)
    print(table)

    table.to_csv("data/metrics.csv", index=False)