from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://dq:dq@localhost/dq_observer")

# only the columns that exist in the database table
COLUMNS = ["file", "row_count", "null_rate", "duplicate_rate",
           "cancelled_rate", "score", "verdict", "rule_failures"]


def save_results(table):
    small = table[COLUMNS].copy()
    small["rule_failures"] = small["rule_failures"].apply(", ".join)
    small.to_sql("batch_results", engine, if_exists="append", index=False)