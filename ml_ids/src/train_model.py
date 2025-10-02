import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

def main():
    os.makedirs("models", exist_ok=True)

    df = pd.read_csv("data/processed/train.csv")

    feature_cols = [
        'duration','src_bytes','dst_bytes','wrong_fragment','urgent',
        'protocol_type_enc','service_enc','flag_enc'
    ]

    # Ensure all features exist
    for c in feature_cols + ['label']:
        if c not in df.columns:
            raise ValueError(f"Column missing in train.csv: {c}")

    # Convert all feature columns to numeric (strings -> numbers)
    for c in feature_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    X = df[feature_cols]
    y = df['label'].apply(lambda x: int(x))  # ensure label is int

    if len(X) == 0 or X.isnull().all().all():
        raise ValueError("X is empty! Check train.csv for proper data.")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    with open("models/ml_model.pkl", "wb") as f:
        pickle.dump(clf, f)

    print("✅ Model trained and saved at models/ml_model.pkl")

if __name__ == "__main__":
    main()
