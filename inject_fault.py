import pandas as pd
from pathlib import Path

df= pd.read_csv("data/batches/orders_2026-09-12.csv")
df = df.sample (frac =0.3, random_state=1)
df.to_csv("data/batches/orders_2026-09-12.csv", index=False)

df = pd.read_csv("data/batches/orders_2026-09-18.csv")
df.loc[df.index[:400],"customer_id"]=None
df.to_csv("data/batches/orders_2026-09-18.csv", index=False)

df = pd.read_csv("data/batches/orders_2026-09-23.csv")
df = pd.concat([df,df.head(100)])
df.to_csv("data/batches/orders_2026-09-23.csv", index=False)

# Oct 15: lose 70% of rows
df = pd.read_csv("data/batches/orders_2026-10-15.csv")
df = df.sample(frac=0.3, random_state=1)
df.to_csv("data/batches/orders_2026-10-15.csv", index=False)

# Oct 21: prices 10x too high
df = pd.read_csv("data/batches/orders_2026-10-21.csv")
df["amount"] = df["amount"] * 10
df.to_csv("data/batches/orders_2026-10-21.csv", index=False)

# Oct 27: 300 orders wrongly marked cancelled
df = pd.read_csv("data/batches/orders_2026-10-27.csv")
df.loc[df.index[:300], "status"] = "cancelled"
df.to_csv("data/batches/orders_2026-10-27.csv", index=False)

faults = pd.DataFrame({
    "file": [
        "orders_2026-09-12.csv","orders_2026-09-18.csv",
        "orders_2026-09-23.csv","orders_2026-10-15.csv","orders_2026-10-21.csv",
        "orders_2026-10-27.csv" 
    ],
})
faults.to_csv("data/faults.csv", index=False)