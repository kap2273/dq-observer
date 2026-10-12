from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()   # read .env into the environment

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql+psycopg://{user}:{password}@localhost/{db}")

# only the columns that exist in the database table
COLUMNS = ["file", "row_count", "null_rate", "duplicate_rate",
           "cancelled_rate", "score", "verdict", "rule_failures"]


def save_results(table):
    small = table[COLUMNS].copy()
    small["rule_failures"] = small["rule_failures"].apply(", ".join)
    small.to_sql("batch_results", engine, if_exists="append", index=False)