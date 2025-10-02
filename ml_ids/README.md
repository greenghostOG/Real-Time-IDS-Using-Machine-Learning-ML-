🔹 Project Overview

This project implements a Real-Time Intrusion Detection System (IDS) powered by Machine Learning.

It captures live network traffic, preprocesses it into features, and uses a trained ML model to detect whether packets are Normal or Malicious.

The IDS provides real-time alerts in the console and also logs them into a file for further analysis.

🔹 Objectives

Detect malicious network activity using ML models.

Train on benchmark dataset (NSL-KDD) for intrusion detection.

Capture and analyze live traffic from network interfaces.

Generate alerts and logs for suspicious packets.

Build a modular, reproducible framework for cybersecurity research.

🔹 Methodology / Workflow

1. Dataset Phase

Preprocess NSL-KDD dataset.

Encode categorical features (protocol_type, service, flag).

Train models (Decision Tree, Random Forest).

Save trained model → models/ml_model.pkl.

2. Live Detection Phase

Capture traffic with Scapy.

Extract features from packets.

Feed features into trained ML model.

Predict Normal / Malicious.

Generate alerts in real-time & log results.

📌 Workflow Diagram:

Packet Capture → Feature Extraction → Preprocessing → ML Model → Detection & Alerts

🔹 Tools & Technologies

Programming Language: Python 3.13

Libraries: Scikit-learn, Pandas, NumPy, Matplotlib

Packet Capture: Scapy

Environment: Kali Linux

Other: Logging, Joblib (model persistence), GitHub

🔹 Project Structure

ml-ids/
│
├── data/
│   ├── raw/           # Original datasets
│   └── processed/     # Preprocessed train/test CSVs
│
├── models/            # Saved ML models (ml_model.pkl)
├── scripts/           # Dataset download & preprocess scripts
├── src/               # Source code
│   ├── api_server.py
│   ├── capture.py
│   ├── evaluate.py
│   ├── features.py
│   ├── online_detector.py
│   ├── preprocess.py
│   ├── train_model.py
│   └── utils.py
│
└── requirements.txt   # Python dependencies

🔹 Setup & Installation

1️⃣ Go To ml_ids Folder : 

Make sure you are running this IDS in Kali Linux.

cd ml_ids

2️⃣ Create Virtual Environment : 

python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install Dependencies : 

pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Download & Preprocess Dataset : 

python3 scripts/download_nslkdd.py

# Verify processed files
head -n 10 data/processed/train.csv
head -n 10 data/processed/test.csv

🔹 Running the IDS : 
Step 1: Train the Model

python3 src/train_model.py

👉 Saves model as models/ml_model.pkl

You can this command after running the IDS :

python3 src/train_model.py --dataset data/processed/train.csv --model models/ml_model.pkl

Step 2: Evaluate Model : 

python3 src/evaluate.py --data data/processed/test.csv --model models/ml_model.pkl

Step 3: Capture Packets : 

sudo python3 src/capture.py --iface wlan0 --out data/processed/live_capture.csv --count 500

👉 Captures 500 packets → saves to live_capture.csv

Step 4: Run Real-Time IDS (Final Step) : 

sudo python3 src/online_detector.py --iface wlan0 --model models/ml_model.pkl --log alerts.log

👉 Starts real-time detection on interface wlan0.
👉 Console displays [ALERT] messages.
👉 Alerts also saved in alerts.log.

🔹 Sample Outputs

Classification Report (Evaluation):

              precision    recall  f1-score   support
           1       1.00      1.00      1.00     22544
    accuracy                           1.00     22544
   macro avg       1.00      1.00      1.00     22544
weighted avg       1.00      1.00      1.00     22544

Real-Time Detection (Console):

[ALERT] Malicious packet detected: Ether / IP / TCP 192.168.1.5:443 > 192.168.1.10:54321

Log File (alerts.log):

2025-09-28 01:53:36,013 - WARNING - [ALERT] Malicious packet detected: Ether / IP / UDP / DNS Qry b'example.com'

🔹 Conclusion

Built a fully functional ML-powered IDS.

Achieves high accuracy (~99%) on benchmark dataset.

Supports real-time packet capture and detection.

Provides alerts and logging for network monitoring.

🔹 Future Enhancements

Add support for IPv6 traffic.

Reduce false positives on encrypted HTTPS.

Integrate with SIEM dashboards (e.g., ELK, Splunk).

Use Deep Learning models (LSTM, CNN) for advanced detection.

Deploy as a cloud-based IDS service.


