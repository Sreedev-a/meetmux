# Phase 1 Task 2 — Pre-Project Feature Scope & Profiling

## Objective

Frame a clear classification problem, audit the available signals, prevent leakage, quantify base rates, define honest evaluation discipline and decide whether basic modelling should proceed.

## Problem Statement

Given 30 quantitative features computed from a digitized fine-needle aspirate image, predict whether each breast-mass sample is malignant or benign. One row represents one diagnostic sample.

## Target

The binary `target` is defined by the dataset metadata: `0 = malignant` and `1 = benign`. Malignant is the critical positive class for metric calculation.

## Success Metric

The primary metric is malignant-class recall (`pos_label=0`) because the scoping assumption prioritizes avoiding missed malignant observations. Malignant F1/precision, ROC-AUC and accuracy are secondary. Accuracy is never interpreted without the majority base rate.

## Dataset

The official brief did not specify a dataset, so the scikit-learn Wisconsin Breast Cancer dataset was used as a reproducible real-data demonstration. It is built into scikit-learn, requires no download, and contains 569 rows, 30 numeric predictors and a binary diagnosis target. The committed CSV is an exact reproducible snapshot.

## Feature Profiling

Pandas profiling found zero missing values, zero constant predictors and zero duplicate complete rows. All 30 predictors are vetted for initial modelling. Raw ranges differ substantially and correlated measurement families exist, so later scale-sensitive pipelines need training-fitted standardization and regularization; correlation alone was not treated as leakage.

## Leakage Check

The target and CSV sample index are excluded from `X`. Name and exact-copy checks found no target copies or suspicious outcome fields. Measurements describe cell nuclei at observation time, with no post-outcome predictors. Splitting precedes learned preprocessing.

## Class Balance

There are 212 malignant samples (37.26%) and 357 benign samples (62.74%). This is moderate imbalance. Always predicting benign yields a 62.74% full-data majority accuracy while detecting no malignant cases.

## Train / Validation / Test Split

A fixed `RANDOM_STATE = 42` stratified split creates 398 train rows (148/250 malignant/benign), 85 validation rows (32/53), and 86 untouched test rows (32/54).

## Baseline

On the unseen test split, `DummyClassifier(strategy="most_frequent")` achieved 62.79% accuracy, 0.00 malignant recall, precision and F1, and 0.50 malignant ROC-AUC. Any useful model must materially beat zero malignant recall, not merely majority accuracy.

## Go / No-Go Decision

**GO** for controlled modelling and validation; **not approved for clinical deployment**. Labels and features are usable, leakage and missingness are controlled, and imbalance is manageable, but deployment would require external validation and clinical governance.

## Proposed Modelling Approach

First use a pipeline with training-fitted `StandardScaler` and class-weighted logistic regression for interpretability; compare a random forest for nonlinear effects. Select thresholds on validation data and evaluate once on test data. No tuning belongs in this scope task.

## Project Structure

```text
data/       reproducible real-data CSV
src/        loading, profiling, leakage and splitting modules
reports/    scope, profiles, leakage, balance and decision
outputs/    three plots and machine-readable summary
tests/      automated reproducibility and integrity checks
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Running the Notebook

```bash
jupyter nbconvert --to notebook --execute --inplace task2_feature_profiling.ipynb
jupyter notebook task2_feature_profiling.ipynb
```

## Running the Python Analysis

```bash
python run_analysis.py
```

## Running Tests

```bash
python -m pytest -q
```

## Generated Outputs

`class_balance.png` shows observed labels, `missing_values.png` demonstrates zero missingness across all predictors, and `feature_summary.png` shows the ten highest raw variances as a range diagnostic (not importance). CSV/Markdown reports retain auditable statistics and decisions.

## Definition of Done

The crisp scope, precise target, metric, 30 vetted features, leakage audit, class-balance report, executed real-data notebook, baseline, reproducible split and GO/no-go decision are all present and demoable.
