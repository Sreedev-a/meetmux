# Submission

**Task:** Phase 1 Task 2

**Title:** Pre-Project Feature Scope & Profiling

## Scope and findings

The objective was to define a prediction target, metric, vetted feature set, leakage audit, balance report and reproducible evaluation discipline. The official brief did not specify a dataset, so the scikit-learn Wisconsin Breast Cancer dataset was used as a reproducible real-data demonstration.

- Target: `0 = malignant`, `1 = benign`; primary metric: malignant-class recall.
- Data: 569 rows, 30 numeric candidate features, zero missing values and zero duplicate complete rows.
- Vetted features: all 30 image-derived measurements; target and sample index are excluded from predictors.
- Leakage: no direct target leakage, target copies, suspicious outcome fields or post-outcome predictors identified.
- Balance: 212 malignant (37.26%), 357 benign (62.74%); majority rate 62.74%.
- Split: stratified with seed 42 into 398 train, 85 validation and 86 test rows.
- Baseline: most-frequent DummyClassifier produced 62.79% test accuracy, 0.00 malignant recall/F1/precision and 0.50 ROC-AUC.
- Decision: GO for controlled modelling, not clinical deployment. Next compare standardized class-weighted logistic regression with random forest.

## Files and outputs

Reusable code is in `src/`; profiles and decisions are in `reports/`; the real-data snapshot is `data/dataset_used.csv`; three charts and the machine-readable summary are in `outputs/`; and the executed notebook plus tests provide demonstrations.

## Commands and tests

```bash
python run_analysis.py
jupyter nbconvert --to notebook --execute --inplace task2_feature_profiling.ipynb
python -m pytest -q
```

Submit the complete `Phase1_Task02_Pre_Project_Feature_Scope_and_Profiling/` folder. Useful screenshots show the notebook summary, the three plots, feature profile, leakage report, baseline metrics and passing tests.
