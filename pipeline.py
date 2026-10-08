from rule import check_rules 
from profile_batch import profile
from anomaly import detect_anomalies
from pathlib import Path
import pandas as pd
from report import build_report

results = []
files = sorted(Path("data/batches").glob("orders_*.csv"))
for f in files:
    df = pd.read_csv(f)
    failures = check_rules(df)
    metrics = profile(f)
    metrics["rule_failures"] = failures
    results.append(metrics)
table = pd.DataFrame(results)


table["score"] = detect_anomalies(table)
THRESHOLD = 0.03
verdict = []
for i, row in table.iterrows():
    if len(row["rule_failures"]) > 0:
        verdict.append("Block")
    elif row["score"] > THRESHOLD:
        verdict.append("Warn")
    else: 
        verdict.append("Pass")
table["verdict"] = verdict

print(table[["file","rule_failures","score","verdict"]])

build_report(table)