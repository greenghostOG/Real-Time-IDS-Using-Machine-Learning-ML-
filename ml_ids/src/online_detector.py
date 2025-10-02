import argparse
import pandas as pd
from scapy.all import sniff, IP
import joblib
from features import packet_to_features
from utils import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Real-time ML IDS")
    parser.add_argument("--iface", required=True, help="Network interface")
    parser.add_argument("--model", required=True, help="Trained ML model")
    parser.add_argument("--log", default=None, help="Optional log file")
    args = parser.parse_args()

    logger = setup_logger("online_detector", args.log)

    model = joblib.load(args.model)
    print(f"Starting live IDS on {args.iface} (IPv4 only). Press Ctrl+C to stop")

    def process_packet(pkt):
        if not pkt.haslayer(IP):
            return  # skip non-IPv4

        df = packet_to_features(pkt)
        if df is None:
            return

        prediction = model.predict(df)[0]
        if prediction == 1:
            msg = f"[ALERT] Malicious packet detected: {pkt.summary()}"
            print(msg)
            if args.log:
                logger.warning(msg)

    sniff(iface=args.iface, prn=process_packet, store=False)

if __name__ == "__main__":
    main()
