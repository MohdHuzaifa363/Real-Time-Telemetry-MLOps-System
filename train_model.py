import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

print("🤖 MLOps Model Training & Validation Protocol Active...\n")

if not os.path.isfile("server_metrics.csv"):
    print("❌ Critical Error: 'server_metrics.csv' data vector matrix not found!")
    exit()

# 1. Load Structured Feature Store matrix
df = pd.read_csv("server_metrics.csv")

# 2. Check if we have enough statistical observations
if len(df) < 10:
    print("⚠️ Data density too low. Please run generatorupdate.py for 1-2 minutes first!")
    exit()

# 3. Segmenting Input Vectors (X) and Target Vector Label (y)
X = df[["CPU_Usage", "RAM_Usage", "Response_Time"]]
y = df["Status"]

# 4. Stratified Data Partitioning (80-20 Train-Test Distribution split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"📊 Training Matrix Size: {X_train.shape[0]} samples | Testing Matrix Size: {X_test.shape[0]}")

# 5. Algorithmic Topography: Random Forest Classifier (Ensemble Topology)
# Initializing 10 independent Decision Trees with Gini impurity splitting criterion
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluation and Statistical Classification Matrix Auditing
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"🎯 Algorithmic Accuracy: {acc * 100:.2f}%")

# Comprehensive metrics output including Precision, Recall, and F1-Score arrays
print("\n📝 Execution Performance Audit Metadata Matrix:")
print(classification_report(y_test, y_pred))

# 7. Serializing the Model Engine (Binary Object Persistence)
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("💾 Serialized Machine Learning Model Object successfully compiled into 'model.pkl'.")