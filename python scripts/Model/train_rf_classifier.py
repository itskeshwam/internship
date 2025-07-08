import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("/home/kali/CICFlowMeter/csv/FLNetMini_master.csv")

# Clean missing values
df = df.dropna(subset=[
    "tcp.len", "tcp.window_size_value", "ip.ttl",
    "PayloadEntropy", "tcp.flags.syn", "tcp.flags.ack", "tcp.flags.fin"
])

# Select features
feature_cols = [
    "tcp.len", "tcp.window_size_value", "ip.ttl", "PayloadEntropy",
    "tcp.flags.syn", "tcp.flags.ack", "tcp.flags.fin"
]
X = df[feature_cols]
y = df["Label"]

# Encode string labels to numbers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
y_test_labels = encoder.inverse_transform(y_test)
y_pred_labels = encoder.inverse_transform(y_pred)

print("✅ Classification Report:")
print(classification_report(y_test_labels, y_pred_labels))

# Confusion Matrix
cm = confusion_matrix(y_test_labels, y_pred_labels, labels=encoder.classes_)
plt.figure(figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=encoder.classes_,
            yticklabels=encoder.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()
