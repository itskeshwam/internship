import pandas as pd

# Load raw CSV
df = pd.read_csv("/home/kali/CICFlowMeter/csv/syn_flood_extracted.csv")

# Drop rows with missing critical fields
df.dropna(subset=['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 'frame.time_epoch'], inplace=True)

# Create Flow ID
df['FlowID'] = df['ip.src'].astype(str) + '-' + df['ip.dst'].astype(str) + '-' + \
               df['tcp.srcport'].astype(str) + '-' + df['tcp.dstport'].astype(str) + '-TCP'

# Estimate payload entropy (approximate)
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

# Labeling logic
def label_row(row):
    syn = int(row.get("tcp.flags.syn", 0))
    ack = int(row.get("tcp.flags.ack", 0))
    fin = int(row.get("tcp.flags.fin", 0))
    length = int(row.get("tcp.len", 0)) if not pd.isna(row.get("tcp.len", 0)) else 0

    if syn == 1 and ack == 0 and fin == 0 and length == 0:
        return "DDoS_TCP_SYN", "SYN-only, no payload"
    elif syn == 1 and ack == 1:
        return "Likely_SYN-ACK", "SYN+ACK packet"
    else:
        return "Unlabeled", "Did not match SYN pattern"

df[['Label', 'LabelReason']] = df.apply(label_row, axis=1, result_type="expand")

# Add filename for traceability
df['SourceFile'] = "syn_flood.pcap"

# Save final enriched dataset
df.to_csv("/home/kali/CICFlowMeter/csv/syn_flood_enriched.csv", index=False)

print("✅ Enrichment complete. File saved as syn_flood_enriched.csv")
