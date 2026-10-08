from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(table):

    X= table[["row_count","null_rate","duplicate_rate","amount_mean","amount_max","cancelled_rate"]]

    model=IsolationForest(random_state=42)
    model.fit(X)
    score=-model.decision_function(X)
    return score

if __name__=="__main__":
    df=pd.read_csv("data/metrics.csv")
    df["score"]= detect_anomalies(df)
    df=df.sort_values("score",ascending=False)
    df["flagged"]= df["score"]>0 
    print(df[["file","score","flagged"]])
