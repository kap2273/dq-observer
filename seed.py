# ============================================================
# seed.py
# PURPOSE: Create 30 days of fake store orders (one CSV per day).
# This is our "normal" data. Later, we'll break some days on
# purpose and check if our inspector catches the problems.
# ============================================================

# --- Bring in toolboxes ---
import numpy as np          # numpy = math + random numbers
import pandas as pd         # pandas = tables (like Excel in Python)
from pathlib import Path    # Path = work with folders and file names

# --- Set up the random number generator ---
# The 42 is a "seed": it makes the random numbers come out
# the SAME every time we run this, so our data is repeatable.
rng = np.random.default_rng(42)

# --- Create the folder where files will be saved ---
# exist_ok=True means "don't crash if the folder already exists"
out = Path("data/batches")
out.mkdir(parents=True, exist_ok=True)

# --- Starting values ---
start = pd.Timestamp("2026-09-01")   # the first day of fake data
order_id = 1                         # the first order number

# --- Repeat once per day, 30 times (day = 0, 1, 2, ... 29) ---
for day in range(30):

    # Today's date = Sept 1 + however many days we've done
    date = start + pd.Timedelta(days=day)

    # Pick how many orders today has (random, between 900 and 1100)
    # so every day is a little different, like a real store
    n = rng.integers(900, 1100)

    # Build today's table. Each line below is one column.
    df = pd.DataFrame({
        # Order numbers in a row, continuing from yesterday
        "order_id": range(order_id, order_id + n),

        # A random customer number (1 to 5000) for each order
        "customer_id": rng.integers(1, 5000, n),

        # Pick a status for each order:
        # 50% placed, 45% shipped, 5% cancelled
        "status": rng.choice(["placed", "shipped", "cancelled"], n, p=[0.5, 0.45, 0.05]),

        # Prices: average $60, usually within ±$20,
        # never below $1, rounded to cents
        "amount": rng.normal(60, 20, n).clip(1).round(2),

        # Today's date on every row
        "order_date": date.date(),
    })

    # Move the order counter forward so tomorrow's
    # order numbers don't repeat today's
    order_id += n

    # Save today's table as a CSV file, e.g. orders_2026-09-01.csv
    # index=False = don't add an extra row-number column
    df.to_csv(out / f"orders_{date.date()}.csv", index=False)

# --- Runs once, after all 30 days are done ---
print("Made 30 batches in", out)