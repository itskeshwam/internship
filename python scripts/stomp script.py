import pandas as pd

df = pd.read_csv("/home/kali/CICFlowMeter/csv/stomp_flood_extracted.csv")

# Remove incomplete rows
df.dropna(subset=['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 'frame.time_epoch'], inplace=True)

# Flow ID (session-aware)
df['FlowID'] = df['ip.src'].astype(str) + '-' + df['ip.dst'].astype(str) + '-' + \
               df['tcp.srcport'].astype(str) + '-' + df['tcp.dstport'].astype(str) + '-TCP'

# Entropy proxy from tcp.len
def fake_entropy(length):
    if pd.isna(length) or length == 0:
        return 0.0
    if length > 1000:
        return 7.5
    elif length > 100:
        return 6.0
    elif length > 10:
        return 4.5
    else:
        return 2.0

df['PayloadEntropy'] = df['tcp.len'].fillna(0).apply(fake_entropy)

# Labeling logic for STOMP
def label_row(row):
    tcp_flags = str(row.get("tcp.flags", ""))
    entropy = float(row.get("PayloadEntropy", 0))
    length = int(row.get("tcp.len", 0)) if not pd.isna(row.get("tcp.len")) else 0
    ack = int(row.get("tcp.flags.ack", 0))
    src = row.get("ip.src", "")
    
    # Heuristic for DDoS_HTTP_STOMP
    if "0x0018" in tcp_flags and length > 0 and entropy >= 4.5:
        return "DDoS_HTTP_STOMP", "PSH+ACK with payload"
    elif ack == 1 and length == 0:
        return "Likely_HTTP_Response", "ACK with no payload"
    else:
        return "Unlabeled", "Default fallback"

df[['Label', 'LabelReason']] = df.apply(label_row, axis=1, result_type="expand")
df['SourceFile'] = "stomp_flood.pcap"

# Save output
df.to_csv("/home/kali/CICFlowMeter/csv/stomp_flood_enriched.csv", index=False)

print("✅ STOMP enrichment complete: stomp_flood_enriched.csv generated")
