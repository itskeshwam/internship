import pandas as pd

# Paths
syn = pd.read_csv("/home/kali/CICFlowMeter/csv/syn_flood_enriched.csv")
stomp = pd.read_csv("/home/kali/CICFlowMeter/csv/stomp_flood_enriched.csv")

# Merge
df = pd.concat([syn, stomp], ignore_index=True)

# Add global unique ID per packet
df.insert(0, "RowID", range(1, len(df) + 1))

# Save
df.to_csv("/home/kali/CICFlowMeter/csv/FLNetMini_master.csv", index=False)

print(f"✅ Combined dataset created with {len(df)} packets → FLNetMini_master.csv")
