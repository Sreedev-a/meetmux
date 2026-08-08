# Fairness audit plan

The audit starts with group outcome diagnostics over recommendation selection. It excludes protected attributes from ranking inputs and uses them only in access-controlled offline evaluation. Review selection rates, score distributions, false-negative rates, and intersectional slices once sample sizes are sufficient. Investigate flagged gaps for label, coverage, threshold, and measurement bias; do not infer causality from ratios alone. A human owner must document remediation, privacy basis, and approval before production changes.
