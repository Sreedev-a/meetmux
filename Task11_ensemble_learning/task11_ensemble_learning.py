import random
import numpy as np
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score

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

# -----------------------------
# Base Models
# -----------------------------

lr = LogisticRegression(max_iter=5000)
dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(random_state=42)

models = {
    "Logistic Regression": lr,
    "Decision Tree": dt,
    "Random Forest": rf
}

best_accuracy = 0
best_model = ""

print("Single Model Performance\n")

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)

    print(f"{name}: {acc:.4f}")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = name

print("\nBest Single Model:", best_model)
print("Best Accuracy:", round(best_accuracy,4))

# -----------------------------
# Ensemble
# -----------------------------

ensemble = VotingClassifier(
    estimators=[
        ("lr", lr),
        ("dt", dt),
        ("rf", rf)
    ],
    voting="hard"
)

ensemble.fit(X_train, y_train)

ensemble_pred = ensemble.predict(X_test)

ensemble_acc = accuracy_score(y_test, ensemble_pred)

print("\nEnsemble Accuracy:", round(ensemble_acc,4))

lift = ensemble_acc - best_accuracy

print("Lift:", round(lift,4))

joblib.dump(ensemble,"ensemble_model.joblib")

print("\nModel saved successfully.")