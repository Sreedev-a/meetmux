# Phase 3 Task 24 — Launch Rehearsal

```bash
MPLCONFIGDIR=/private/tmp/mplconfig ../ml_env/bin/python fairness_signoff.py
../ml_env/bin/python -m unittest -v test_fairness_signoff.py
```

This closes the fairness audit with a fail-closed model sign-off. No production audit log was present, so the execution uses a clearly labeled deterministic fallback fixture.
