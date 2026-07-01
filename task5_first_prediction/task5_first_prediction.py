from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from collections import Counter
import random
import numpy as np

# Reproducibility
random.seed(42)
np.random.seed(42)

# Load dataset
iris = load_iris()

X = iris.data
y = iris.target

# Split data
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.5,
    random_state=42
)

# --------------------
# Baseline Model
# --------------------

majority_class = Counter(y_train).most_common(1)[0][0]

baseline_predictions = [majority_class] * len(y_val)

baseline_accuracy = accuracy_score(
    y_val,
    baseline_predictions
)

print("Baseline Accuracy:", baseline_accuracy)

# --------------------
# Decision Tree
# --------------------

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

predictions = model.predict(X_val)

accuracy = accuracy_score(y_val, predictions)

print("Validation Accuracy:", accuracy)

print("\nWorst Errors:")

for actual, pred in zip(y_val, predictions):
    if actual != pred:
        print(f"Actual={actual} Predicted={pred}")