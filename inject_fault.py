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