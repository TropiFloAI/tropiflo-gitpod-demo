#!/usr/bin/env python3
import os
import time
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix, classification_report
import fsspec

start_time = time.time()

INPUT_URI = os.environ.get("INPUT_URI")

# Load training data using fsspec
train_csv_path = os.path.join(INPUT_URI, "sp500.csv")
print(f"Loading data from: {train_csv_path}")
with fsspec.open(train_csv_path, "rt") as f:
    df = pd.read_csv(f)
# Config
TRAIN_FRAC = 0.70
RANDOM_STATE = 42

# CO_DATASCIENTIST_BLOCK_START

# Features
df["ret_1d"] = df["close"].pct_change()
df["mom_5d"] = df["close"].pct_change(5)
df["vol_10d"] = df["ret_1d"].rolling(10).std()
ma5 = df["close"].rolling(5).mean()
ma20 = df["close"].rolling(20).mean()
spread = ma5 - ma20
df["ma_spread_z"] = (spread - spread.rolling(60).mean()) / (spread.rolling(60).std() + 1e-12)
# Lag features by 1 day (no look-ahead)
for c in ["ret_1d", "mom_5d", "vol_10d", "ma_spread_z"]:
    df[f"{c}_lag1"] = df[c].shift(1)
# Target: next-day up (1) else 0
df["y"] = (df["close"].shift(-1) > df["close"]).astype(int)
feat_cols = [c for c in df.columns if c.endswith("_lag1")]


# CO_DATASCIENTIST_BLOCK_END

data = df[feat_cols + ["y"]].dropna().copy()

# Split
n = len(data)
n_train = int(n * TRAIN_FRAC)
X_train = data.iloc[:n_train][feat_cols]
y_train = data.iloc[:n_train]["y"].astype(int)
X_test = data.iloc[n_train:][feat_cols]
y_test = data.iloc[n_train:]["y"].astype(int)

# Model
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=200, random_state=RANDOM_STATE))
])
model.fit(X_train, y_train)

# Evaluate
proba = model.predict_proba(X_test)[:, 1]
preds = (proba >= 0.5).astype(int)
acc = accuracy_score(y_test, preds)
prec = precision_score(y_test, preds, zero_division=0)
rec = recall_score(y_test, preds)
auc = roc_auc_score(y_test, proba)
cm = confusion_matrix(y_test, preds)

print(f"KPI: {auc:.6f}")

end_time = time.time()
print(f"Total runtime: {end_time - start_time:.2f} seconds")
