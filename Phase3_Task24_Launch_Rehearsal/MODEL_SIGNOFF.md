# Model sign-off — recommendation gate v2.0.0

Decision: approved for controlled launch rehearsal, subject to production monitoring.

The gate requires at least 200 evaluation records per audit group, overall accuracy ≥ 0.80, disparate-impact ratio ≥ 0.80, equal-opportunity gap ≤ 0.10, false-positive-rate gap ≤ 0.10, a verified artifact checksum, and named ownership. `outputs/fairness_signoff.json` is the authoritative executed evidence. Sensitive audit groups are evaluation-only and remain excluded from model inputs.

Rollback triggers: any production quality/SLO breach, material segment gap, input drift, integrity failure, or missing monitoring. Owner: ML Reliability Owner. Review cadence: weekly for the first month, then monthly.
