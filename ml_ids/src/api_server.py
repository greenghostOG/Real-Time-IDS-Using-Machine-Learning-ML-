from flask import Flask, request, jsonify
from joblib import load
from preprocess import preprocess
import pandas as pd

app = Flask(__name__)
model = load("models/rf_model.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    X = preprocess(df)
    pred = model.predict(X)[0]
    return jsonify({"prediction": "malicious" if pred else "benign"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
