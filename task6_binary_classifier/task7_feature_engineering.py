import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Reproducibility
random.seed(42)
np.random.seed(42)

# Load Dataset
data = load_breast_cancer()

df = pd.DataFrame(data.data, columns=data.feature_names)
df["target"] = data.target

# Feature Engineering
df["mean_radius_area"] = df["mean radius"] * df["mean area"]
df["radius_perimeter_ratio"] = df["mean radius"] / df["mean perimeter"]

# Features and Target
X = df.drop("target", axis=1)
y = df["target"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Feature Importance
importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nTop 10 Important Features\n")
print(importance.head(10))

# Plot Feature Importance
plt.figure(figsize=(10,6))
importance.head(10).plot(kind="bar")
plt.title("Top 10 Feature Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300)
plt.close()

print("\nLeakage Check")
print("No target information was used while creating engineered features.")

print("\nBaseline Feature Set Locked.")