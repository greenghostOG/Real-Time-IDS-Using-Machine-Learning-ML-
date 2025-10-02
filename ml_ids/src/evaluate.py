import argparse
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from joblib import load
from preprocess import preprocess
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.data) or not os.path.exists(args.model):
        raise FileNotFoundError("Data or model path not found.")

    df = pd.read_csv(args.data)
    y = df['label']
    X = preprocess(df)

    model = load(args.model)
    preds = model.predict(X)

    print("=== Classification Report ===")
    print(classification_report(y, preds))
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y, preds))

if __name__ == "__main__":
    main()
