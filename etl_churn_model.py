#!/usr/bin/env python3
"""ETL + Churn Model (LogReg)
- Loads synthetic data (or your own CSV)
- Trains a logistic regression on churn label
- Saves scaler & model
- Scores and exports a Tableau-ready CSV
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
import joblib

DATA = Path("data/synthetic_customers.csv")
MODELS = Path("models")
OUT = Path("out")
MODELS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA)
    features = ["tenure_days","last_nps","tickets_30d","usage_delta","sentiment_score","plan","region","billing_change_30d"]
    target = "churned_next_60d"
    X = df[features]
    y = df[target]

    num_cols = ["tenure_days","last_nps","tickets_30d","usage_delta","sentiment_score"]
    cat_cols = ["plan","region","billing_change_30d"]
    pre = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ])
    clf = LogisticRegression(max_iter=200, n_jobs=None, class_weight="balanced")
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    pipe.fit(X, y)

    # Evaluate
    pred_proba = pipe.predict_proba(X)[:,1]
    auc = roc_auc_score(y, pred_proba)
    print(f"AUC: {auc:.3f}")
    print(classification_report(y, (pred_proba>0.5).astype(int)))

    # Persist
    joblib.dump(pipe, MODELS / "churn_logit_pipeline.joblib")
    # Export scores for Tableau
    export = df[["customer_id","plan","region"]].copy()
    export["churn_prob"] = pred_proba
    export.to_csv(OUT / "churn_scores.csv", index=False)
    print("Saved model to models/churn_logit_pipeline.joblib and scores to out/churn_scores.csv")

if __name__ == "__main__":
    main()
