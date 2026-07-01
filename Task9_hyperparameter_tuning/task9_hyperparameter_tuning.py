import random
import numpy as np
import pandas as pd
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Reproducibility
random.seed(42)
np.random.seed(42)

# Load Dataset
data = load_breast_cancer()

X = data.data
y = data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ------------------------
# Baseline Model
# ------------------------

baseline = RandomForestClassifier(random_state=42)

baseline.fit(X_train, y_train)

baseline_pred = baseline.predict(X_test)

baseline_acc = accuracy_score(y_test, baseline_pred)

print(f"Baseline Accuracy : {baseline_acc:.4f}")

# ------------------------
# Hyperparameter Search
# ------------------------

param_grid = {
    "n_estimators":[50,100,200],
    "max_depth":[None,5,10],
    "min_samples_split":[2,5,10]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train,y_train)

best_model = grid.best_estimator_

pred = best_model.predict(X_test)

best_acc = accuracy_score(y_test,pred)

print(f"Tuned Accuracy    : {best_acc:.4f}")

print("\nBest Parameters")
print(grid.best_params_)

print(f"\nImprovement : {best_acc-baseline_acc:.4f}")

# Save CV Results
results = pd.DataFrame(grid.cv_results_)
results.to_csv("cv_results.csv",index=False)

# Save Model
joblib.dump(best_model,"best_model.joblib")

print("\nArtifacts Saved Successfully")