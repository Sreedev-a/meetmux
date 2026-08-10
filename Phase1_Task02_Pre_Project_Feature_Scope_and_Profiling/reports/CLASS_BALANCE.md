# Class Balance and Base Rates

| Class | Meaning | Count | Percentage |
|---:|---|---:|---:|
| 0 | malignant | 212 | 37.26% |
| 1 | benign | 357 | 62.74% |
| **Total** | | **569** | **100.00%** |

The majority-class baseline is **62.74% accuracy** by always predicting benign. The data are moderately, not strongly, imbalanced: malignant cases remain a substantial 37.26%. Raw accuracy alone is misleading because the majority baseline achieves 62.74% while detecting no malignant samples. Stratification preserves these base rates in the 398/85/86 train/validation/test split.
