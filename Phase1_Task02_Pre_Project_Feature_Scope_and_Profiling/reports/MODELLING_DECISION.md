# Modelling Decision

## Decision

**GO** for controlled baseline modelling and validation; **not approved for clinical deployment**.

The target and class meanings are explicit, 569 labelled observations support a basic demonstration, all 30 numeric predictors are usable, no values are missing, no duplicate complete rows exist, and no direct target leakage was identified. Moderate imbalance is manageable through stratification, malignant-focused metrics and possible class weighting. Generalization and clinical validity still require independent external data, governance and domain review.

## Reproducible split

Using `RANDOM_STATE = 42` and stratification:

| Split | Rows | Malignant | Benign |
|---|---:|---:|---:|
| Train | 398 | 148 | 250 |
| Validation | 85 | 32 | 53 |
| Test | 86 | 32 | 54 |

The test set remains untouched until final evaluation. Any scaler, imputer or learned transformation must be fitted on training data only.

## Baseline

On the unseen 86-row test split, `DummyClassifier(strategy="most_frequent")` achieved **62.79% accuracy**, **0.00 malignant recall**, **0.00 malignant precision**, **0.00 malignant F1**, and **0.50 malignant ROC-AUC**. This honest baseline shows why accuracy is secondary: always predicting benign detects none of 32 malignant test cases. A useful model must materially exceed zero malignant recall while managing precision.

## Proposed next approach

Start with a pipeline containing training-fitted `StandardScaler` and class-weighted logistic regression for an interpretable linear baseline. Compare it with a random forest for nonlinear interactions. Select thresholds on validation data using malignant recall plus F1/precision trade-offs, evaluate once on the test set, and avoid hyperparameter tuning in this scoping task.
