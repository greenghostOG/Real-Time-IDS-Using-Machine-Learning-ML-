import argparse, pandas as pd
from scapy.all import sniff
from features import packet_to_features
from utils import setup_logger

logger = setup_logger("capture")
rows = []

def handle_pkt(pkt):
    global rows
    feats = packet_to_features(pkt)
    rows.append(feats)
    if len(rows) % 100 == 0:
        logger.info(f"Captured {len(rows)} packets")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iface", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--count", type=int, default=0)
    args = parser.parse_args()

    sniff(iface=args.iface, prn=handle_pkt, store=0, count=args.count)

    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(args.out, index=False)
        logger.info(f"Saved {len(rows)} packets to {args.out}")

if __name__ == "__main__":
    main()
