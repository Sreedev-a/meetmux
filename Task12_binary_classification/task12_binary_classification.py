import random
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Reproducibility
random.seed(42)
np.random.seed(42)

# Load dataset
data = load_breast_cancer()

X = data.data
y = data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Base classifier
base_model = LogisticRegression(max_iter=5000)

# Probability calibration
model = CalibratedClassifierCV(base_model, cv=5)

model.fit(X_train, y_train)

# Predicted probabilities
probabilities = model.predict_proba(X_test)[:,1]

# Decision threshold
threshold = 0.50

predictions = (probabilities >= threshold).astype(int)

# Metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall : {recall:.4f}")
print(f"Operating Threshold : {threshold}")

# Calibration Curve
CalibrationDisplay.from_estimator(
    model,
    X_test,
    y_test
)

plt.tight_layout()
plt.savefig("calibration_curve.png", dpi=300)
plt.close()

# Save model
joblib.dump(model, "calibrated_model.joblib")

print("\nArtifacts Generated Successfully")