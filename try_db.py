import pandas as pd
from sqlalchemy import create_engine

# the database's address
engine = create_engine("postgresql+psycopg://dq:dq@localhost/dq_observer")

# one fake row
row = pd.DataFrame({
    "file": ["test.csv"],
    "verdict": ["Pass"],
})

# put it in the batch_results table
row.to_sql("batch_results", engine, if_exists="append", index=False)

print("Saved!")