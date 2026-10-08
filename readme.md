# Data Quality Observer

A Python pipeline that checks each day's batch of order data before it's used, combining **explicit rules** (for problems you can predict) with an **anomaly detection model** (for problems you can't).

Each daily batch gets one verdict:

| Verdict | Meaning |
|---|---|
| **BLOCK** | A rule was broken. The data is wrong and should not be used. |
| **WARN** | No rule broken, but the batch looks unusual compared to past days. |
| **PASS** | Looks healthy. |

## How it works

```
 daily orders CSV
        │
        ├──► check_rules()   → broken rule?       → BLOCK
        │
        └──► profile()       → batch metrics
                  │
                  ▼
           detect_anomalies() → score > threshold? → WARN
                                                     else PASS
```

**Rules** check things that should never happen: duplicate order IDs, blank customer IDs, negative amounts, unknown status values.

**The anomaly model** (scikit-learn Isolation Forest) learns what a normal day looks like from 30 days of batch metrics (row count, null rate, duplicate rate, average and max amount, cancellation rate) and scores how unusual each day is.

### Why both?

Rules alone miss problems where nothing in the file is *wrong*, only *missing*. In testing, a batch that lost 70% of its rows passed every rule, because every remaining row was valid. The anomaly model caught it.

## Quick start

Tested on Ubuntu 26.04 (WSL) with Python 3.14.

```bash
git clone <this-repo-url>
cd dq-observer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python seed.py           # generate 30 days of clean synthetic orders
python inject_fault.py   # break 3 days on purpose (run once after seeding)
python pipeline.py       # run rules + anomaly model, print verdicts
```

## Demo scenario

`inject_fault.py` introduces three controlled faults:

| Day | Fault | Real-world cause it simulates |
|---|---|---|
| Sept 12 | 70% of rows removed | Upload failed partway |
| Sept 18 | `customer_id` blanked on 400 rows | Upstream system stopped sending a field |
| Sept 23 | 100 orders duplicated | Job ran twice |

## Results

On 30 synthetic daily batches with a score threshold of 0.03:

| Day | Caught by | Verdict |
|---|---|---|
| Sept 12 | Anomaly model | WARN |
| Sept 18 | Rules | BLOCK |
| Sept 23 | Rules | BLOCK |
| Other 27 days | n/a | PASS |

All 3 injected faults were caught with no false alarms on clean days.

## Design decisions

- **Rules run on raw data, not averaged metrics.** Sept 18 had 37% of `customer_id` blank, but the table-wide null rate was only ~7%. Checking the column directly avoids that dilution.
- **`amount_min` is excluded from the model.** Synthetic prices are clipped at $1.00, so nearly every day has the same minimum. Any day without a $1 order looked unusual and caused a false alarm.
- **Anomalies warn, rules block.** Rules are certain; the model only says "this looks odd," so it flags for review instead of stopping the data.

## Limitations

- Synthetic data only.
- The threshold was chosen by looking at the same 30 days it's evaluated on. A fair test would tune it on earlier days and evaluate on later ones.
- `inject_fault.py` is not idempotent: running it twice without reseeding damages data twice.
- Results are printed, not stored.

## Project files

| File | Purpose |
|---|---|
| `seed.py` | Generate 30 days of synthetic orders |
| `inject_fault.py` | Break specific days on purpose |
| `profile_batch.py` | `profile()`: measure one batch |
| `rule.py` | `check_rules()`: explicit data rules |
| `anomaly.py` | `detect_anomalies()`: Isolation Forest scoring |
| `pipeline.py` | Run everything and assign verdicts |

## Next steps

- Store results in PostgreSQL
- HTML report of verdicts and score trends
- Automated tests with pytest
- Chronological evaluation for threshold tuning
- Scheduling with Airflow in Docker