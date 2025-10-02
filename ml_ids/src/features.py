import pandas as pd
from scapy.all import IP, TCP, UDP

# Mapping functions (example encodings, match what your train_model used)
PROTOCOL_MAP = {"tcp": 0, "udp": 1, "icmp": 2}
SERVICE_MAP = {"http": 0, "dns": 1, "ftp": 2, "other": 3}  # add as per dataset
FLAG_MAP = {"S": 0, "A": 1, "F": 2, "P": 3, "R": 4, "other": 5}

def encode_protocol(pkt):
    if pkt.haslayer(TCP):
        return PROTOCOL_MAP.get("tcp", 2)
    elif pkt.haslayer(UDP):
        return PROTOCOL_MAP.get("udp", 2)
    else:
        return PROTOCOL_MAP.get("icmp", 2)

def encode_service(pkt):
    if pkt.haslayer(TCP) and pkt[TCP].dport == 80:
        return SERVICE_MAP.get("http", 3)
    elif pkt.haslayer(UDP) and pkt[UDP].dport == 53:
        return SERVICE_MAP.get("dns", 3)
    else:
        return SERVICE_MAP.get("other", 3)

def encode_flag(pkt):
    if pkt.haslayer(TCP):
        flags = pkt[TCP].flags
        return FLAG_MAP.get(str(flags), FLAG_MAP["other"])
    return FLAG_MAP["other"]

def packet_to_features(pkt):
    """
    Extract features exactly matching training columns:
    duration, src_bytes, dst_bytes, wrong_fragment, urgent,
    protocol_type_enc, service_enc, flag_enc
    """
    if not pkt.haslayer(IP):
        return None  # skip non-IPv4

    feats = {
        "duration": 0,  # live packets don't have duration
        "src_bytes": len(pkt),
        "dst_bytes": 0,  # cannot measure at capture
        "wrong_fragment": 0,
        "urgent": 0,
        "protocol_type_enc": encode_protocol(pkt),
        "service_enc": encode_service(pkt),
        "flag_enc": encode_flag(pkt)
    }

    return pd.DataFrame([feats])
