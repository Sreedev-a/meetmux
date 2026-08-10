# Leakage Report

Target leakage is information that would be unavailable at prediction time or directly reveals the outcome, producing unrealistically optimistic evaluation.

The `target` column was separated before profiling and splitting. Name screening found 0 suspicious predictor names; exact-copy checks found 0 target copies. The 30 predictors are image-derived nuclear measurements available for the diagnostic observation, with no post-outcome fields or identifiers. No direct target leakage was identified among the candidate predictor features.

Splitting occurs before any learned preprocessing. The dataset has no duplicate complete rows, preventing duplicate observations from crossing splits. Future pipelines must fit imputers/scalers only on training data.

## VETTED_FEATURES

- `mean radius`
- `mean texture`
- `mean perimeter`
- `mean area`
- `mean smoothness`
- `mean compactness`
- `mean concavity`
- `mean concave points`
- `mean symmetry`
- `mean fractal dimension`
- `radius error`
- `texture error`
- `perimeter error`
- `area error`
- `smoothness error`
- `compactness error`
- `concavity error`
- `concave points error`
- `symmetry error`
- `fractal dimension error`
- `worst radius`
- `worst texture`
- `worst perimeter`
- `worst area`
- `worst smoothness`
- `worst compactness`
- `worst concavity`
- `worst concave points`
- `worst symmetry`
- `worst fractal dimension`
