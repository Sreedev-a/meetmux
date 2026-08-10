# Problem Scope

**Given 30 quantitative features computed from a digitized fine-needle aspirate image, predict whether each breast-mass sample is malignant or benign.**

One row is one diagnostic breast-mass sample. This demonstration supports technical scoping only and is not a clinical diagnostic system.

## Target Definition

- Column: `target`
- Type: binary categorical outcome encoded as an integer
- Classes: two
- `0` = malignant (positive/critical class for evaluation)
- `1` = benign (negative/non-critical class for evaluation)

These meanings come directly from scikit-learn's dataset metadata. Eight representative examples are recorded in `manual_label_examples.csv`.

## Success Metric

**Primary metric: malignant-class recall (`pos_label=0`).** Missing a malignant observation is the most consequential classification error under the explicit scoping assumption that false negatives warrant priority. No clinical deployment threshold is claimed.

Secondary metrics are malignant-class F1 and precision, ROC-AUC with malignant treated as positive, and accuracy. F1 captures the precision/recall trade-off; ROC-AUC evaluates ranking across thresholds; accuracy is reported only alongside the 62.74% majority-class base rate because it can conceal complete failure on malignant cases.
