import pandas as pd
from pathlib import Path

def check_rules(df):
    failure  =[]
    if df["order_id"].duplicated().any():
        failure.append("Duplicate order_id found")
    if df["customer_id"].isna().any():
        failure.append("Null customer_id found")
    if df["amount"].min() < 0:
        failure.append("Negative amount found")
    if not df["status"].isin(["placed", "shipped", "cancelled"]).all():
        failure.append("Invalid status found")
    return failure

if __name__ == "__main__":    
    days = ["2026-09-01","2026-09-12", "2026-09-18", "2026-09-23","2026-09-30"]
    for d in days:
        df= pd.read_csv(f"data/batches/orders_{d}.csv")
        print(d, check_rules(df))
