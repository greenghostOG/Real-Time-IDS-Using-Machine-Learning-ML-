# scripts/download_nslkdd.py
import os, requests, pandas as pd
from sklearn.preprocessing import LabelEncoder

os.makedirs("data/raw", exist_ok=True)

urls = {
    "train": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt",
    "test":  "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt",
    "cols":  "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDFeatureNames.txt"
}

paths = {k: f"data/raw/{k}.txt" for k in urls}
for k,u in urls.items():
    if not os.path.exists(paths[k]):
        r = requests.get(u, timeout=30)
        r.raise_for_status()
        open(paths[k], "wb").write(r.content)
        print(f"Downloaded {paths[k]}")

# Read feature names
with open(paths["cols"], "r") as f:
    cols = [line.strip().split()[0] for line in f.readlines()]
cols.append("label")   # total expected cols = len(cols) (should be 42)

EXPECTED_COLS = len(cols)  # usually 42

def parse_file_strict(file_path):
    """Try robust parsing: try comma with maxsplit, then comma, then whitespace fallback."""
    rows = []
    with open(file_path, "r", errors="ignore") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            # 1) Try comma with maxsplit to preserve trailing commas inside label if any
            parts = line.split(",", EXPECTED_COLS - 1)
            if len(parts) == EXPECTED_COLS:
                rows.append(parts)
                continue
            # 2) Try simple comma split
            parts = line.split(',')
            if len(parts) == EXPECTED_COLS:
                rows.append(parts)
                continue
            # 3) Try whitespace split
            parts = line.split()
            if len(parts) == EXPECTED_COLS:
                rows.append(parts)
                continue
            # 4) Try splitting by comma then join extra pieces into final label
            parts = line.split(',')
            if len(parts) > EXPECTED_COLS:
                head = parts[:EXPECTED_COLS-1]
                tail = ",".join(parts[EXPECTED_COLS-1:])
                rows.append(head + [tail])
                continue
            # otherwise skip malformed line
            # (we skip lines that don't match expected columns)
    return rows

# Parse train and test
train_rows = parse_file_strict(paths["train"])
test_rows  = parse_file_strict(paths["test"])

if len(train_rows) == 0:
    raise SystemExit("No valid rows parsed from train file — aborting. Check data/raw/train.txt")

df_train = pd.DataFrame(train_rows, columns=cols)
df_test  = pd.DataFrame(test_rows, columns=cols)

# Convert numeric columns safely, fill missing ones if absent
numeric_cols = ['duration','src_bytes','dst_bytes','wrong_fragment','urgent']
for c in numeric_cols:
    if c in df_train.columns:
        df_train[c] = pd.to_numeric(df_train[c], errors='coerce').fillna(0)
    else:
        df_train[c] = 0
    if c in df_test.columns:
        df_test[c] = pd.to_numeric(df_test[c], errors='coerce').fillna(0)
    else:
        df_test[c] = 0

# Ensure categorical columns exist
cat_cols = ['protocol_type','service','flag']
for c in cat_cols:
    if c not in df_train.columns:
        df_train[c] = 'unknown'
    if c not in df_test.columns:
        df_test[c] = 'unknown'

# Encode categorical safely
for c in cat_cols:
    le = LabelEncoder()
    df_train[c + '_enc'] = le.fit_transform(df_train[c].astype(str))
    # For test, if unseen labels appear it will map accordingly using fit on train
    df_test[c + '_enc'] = le.transform(df_test[c].astype(str))

# Build features (match what train_model expects)
feature_cols = numeric_cols + [c + '_enc' for c in cat_cols]
X_train = df_train[feature_cols]
y_train = df_train['label'].apply(lambda x: 0 if str(x).lower() == "normal" else 1)
X_test  = df_test[feature_cols]
y_test  = df_test['label'].apply(lambda x: 0 if str(x).lower() == "normal" else 1)

os.makedirs("data/processed", exist_ok=True)
pd.concat([X_train, y_train.rename('label')], axis=1).to_csv("data/processed/train.csv", index=False)
pd.concat([X_test,  y_test.rename('label')], axis=1).to_csv("data/processed/test.csv", index=False)

print(f"✅ Parsed {len(train_rows)} train rows and {len(test_rows)} test rows.")
print("Saved data/processed/train.csv and test.csv")
