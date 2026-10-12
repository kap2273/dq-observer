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
results from every run are stored in a PostgreSQL table batch_results, with a timestamp per run.

**The anomaly model** (scikit-learn Isolation Forest) learns what a normal day looks like from 30 days of batch metrics (row count, null rate, duplicate rate, average and max amount, cancellation rate) and scores how unusual each day is.


### Why both?

Rules alone miss problems where nothing in the file is *wrong*, only *missing*. In testing, a batch that lost 70% of its rows passed every rule, because every remaining row was valid. The anomaly model caught it.

## Quick start

Tested on Ubuntu 26.04 (WSL) with Python 3.14.

```bash
git clone <this-repo-url>
cd dq-observer
cp .env.example .env          # then set your own password in .env
docker compose up -d          # start PostgreSQL (table is created automatically)

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python seed.py
python inject_fault.py        # run once after seeding
python pipeline.py
```

## Demo scenario

`inject_fault.py` introduces three controlled faults:

| Day | Fault | Real-world cause it simulates |
|---|---|---|
| Sept 12 | 70% of rows removed | Upload failed partway |
| Sept 18 | `customer_id` blanked on 400 rows | Upstream system stopped sending a field |
| Sept 23 | 100 orders duplicated | Job ran twice |

## Results

### Chronological evaluation

60 daily batches. The model and threshold were fit on the first 40 days (Sept 1 – Oct 10), using only days that passed the rules. It was then evaluated on the last 20 days (Oct 11 – 30), which contain three faults the rules can't catch.

| Day | Fault | Score | Caught? |
|---|---|---|---|
| Oct 15 | 70% of rows lost | 0.186 | Yes |
| Oct 21 | Prices 10× too high | 0.093 | Yes |
| Oct 27 | 300 orders wrongly cancelled | 0.034 | **No** |

Threshold (95th percentile of training scores): 0.047

- Recall: 2 of 3 faults caught
- Precision: 2 of 2 flags were real faults
- False alarms: 0 of 17 clean test days

**Why Oct 27 was missed:** the cancelled-rate spike changes only one of six features, and its score (0.034) is indistinguishable from a clean day (Oct 24, 0.035). Also, Sept 12 (a fault that passes the rules) remained in the training data, which likely raised the threshold.

## Design decisions

- **Rules run on raw data, not averaged metrics.** Sept 18 had 37% of `customer_id` blank, but the table-wide null rate was only ~7%. Checking the column directly avoids that dilution.
- **`amount_min` is excluded from the model.** Synthetic prices are clipped at $1.00, so nearly every day has the same minimum. Any day without a $1 order looked unusual and caused a false alarm.
- **Anomalies warn, rules block.** Rules are certain; the model only says "this looks odd," so it flags for review instead of stopping the data.

## Limitations

- Synthetic data only.
- - Small training window (~37 clean days). Training data may contain undetected faults (Sept 12 does), which inflates the threshold.
- A single-feature shift (like the cancellation spike) can be missed; a dedicated rule or per-feature check would catch it.
- `inject_fault.py` is not idempotent: running it twice without reseeding damages data twice.

## Testing

```bash
pytest
```

| Test file | What it proves |
|---|---|
| `test_rules.py` | Clean data passes; each rule catches its own fault (duplicates, blank customers, negative amounts, invalid status) |
| `test_profile.py` | Metrics match hand-calculated values on a small known table |

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

- HTML report of verdicts and score trends
- Chronological evaluation for threshold tuning
- Scheduling with Airflow in Docker