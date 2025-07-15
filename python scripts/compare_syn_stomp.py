import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
syn_file = "D:\Internship\CICFlowMeter\csv\syn_flood_enriched.csv"
stomp_file = "D:\Internship\CICFlowMeter\csv\stomp_flood_enriched.csv"

# Load
syn = pd.read_csv(syn_file)
stomp = pd.read_csv(stomp_file)

# Add source column for plotting
syn["Attack"] = "SYN Flood"
stomp["Attack"] = "STOMP Flood"
df = pd.concat([syn, stomp], ignore_index=True)

sns.set(style="whitegrid")

# 1. TCP Flags (raw string count)
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="tcp.flags", hue="Attack")
plt.title("TCP Flag Combinations")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("tcp_flags_comparison.png")
plt.close()

# 2. Payload Entropy
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="PayloadEntropy", hue="Attack", kde=True, bins=30)
plt.title("Payload Entropy Distribution")
plt.tight_layout()
plt.savefig("payload_entropy.png")
plt.close()

# 3. Payload Length
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="tcp.len", hue="Attack", kde=False, bins=30)
plt.title("TCP Payload Length")
plt.tight_layout()
plt.savefig("tcp_len_distribution.png")
plt.close()

# 4. TCP Window Size
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x="Attack", y="tcp.window_size_value")
plt.title("TCP Window Size by Attack")
plt.tight_layout()
plt.savefig("window_size_boxplot.png")
plt.close()

# 5. TTL Distribution
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="ip.ttl", hue="Attack", bins=30, kde=True)
plt.title("IP TTL Distribution")
plt.tight_layout()
plt.savefig("ttl_distribution.png")
plt.close()

# 6. Packet Count by Label
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="Label", hue="Attack")
plt.title("Packet Count by Label Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("label_counts.png")
plt.close()

# 7. Top FlowIDs (optional deep dive)
top_flows = df["FlowID"].value_counts().head(10)
print("Top 10 Frequent FlowIDs:\n", top_flows)

print("✅ All comparison plots saved:")
print("- tcp_flags_comparison.png")
print("- payload_entropy.png")
print("- tcp_len_distribution.png")
print("- window_size_boxplot.png")
print("- ttl_distribution.png")
print("- label_counts.png")

