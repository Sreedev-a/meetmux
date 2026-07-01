import random
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.inspection import PartialDependenceDisplay

# Reproducibility
random.seed(42)
np.random.seed(42)

# Load dataset
data = load_breast_cancer()

X = data.data
y = data.target
feature_names = data.feature_names

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------
# Baseline Model
# -------------------------

baseline = LogisticRegression(max_iter=5000)

baseline.fit(X_train, y_train)

baseline_pred = baseline.predict(X_test)

baseline_acc = accuracy_score(y_test, baseline_pred)

print(f"Baseline Accuracy : {baseline_acc:.4f}")

# -------------------------
# Gradient Boosting Model
# -------------------------

gb = GradientBoostingClassifier(random_state=42)

gb.fit(X_train, y_train)

gb_pred = gb.predict(X_test)

gb_acc = accuracy_score(y_test, gb_pred)

print(f"Gradient Boosting Accuracy : {gb_acc:.4f}")

print(f"Improvement : {gb_acc-baseline_acc:.4f}")

# Save model
joblib.dump(gb, "best_model.joblib")

# Partial Dependence Plot
fig, ax = plt.subplots(figsize=(8,5))

PartialDependenceDisplay.from_estimator(
    gb,
    X_train,
    [0],
    feature_names=feature_names,
    ax=ax
)

plt.tight_layout()
plt.savefig("partial_dependence.png", dpi=300)
plt.close()

print("\nArtifacts Generated Successfully")