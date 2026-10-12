import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from rule import check_rules
from profile_batch import profile

FEATURES = ["row_count", "null_rate", "duplicate_rate",
            "amount_mean", "amount_max", "cancelled_rate"]

# 1. build the 60-day table (same loop as pipeline.py)
results = []
for f in sorted(Path("data/batches").glob("orders_*.csv")):
    # ______ your 5 loop lines from pipeline.py
    df = pd.read_csv(f)
    failures = check_rules(df)
    metrics = profile(f)
    metrics["rule_failures"] = failures
    results.append(metrics)
table = pd.DataFrame(results)

# 2. split into study and exam
train = table.iloc[:40]
test = table.iloc[40:].copy()

# 3. learn only from study days that passed the rules
train_clean = train[train["rule_failures"].apply(len) == 0]
model = IsolationForest(random_state=42)
model.fit(train_clean[FEATURES])

# 4. pick the threshold from study days only
train_scores = -model.decision_function(train_clean[FEATURES])
threshold = np.quantile(train_scores, 0.95)

# 5. take the exam
test["score"] = -model.decision_function(test[FEATURES])
test["flagged"] = test["score"] > threshold

# 6. check against the answer key
faults = pd.read_csv("data/faults.csv")["file"]
test["is_fault"] = test["file"].isin(faults)

print("threshold:", round(threshold, 4))
print(test[["file", "score", "flagged", "is_fault"]].sort_values("score", ascending=False).head(8))