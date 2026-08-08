# Phase 3 Sprint A Task 5 — Reliability Sign-off & Scale Integration

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/mplconfig ../ml_env/bin/python signoff.py
MPLCONFIGDIR=/private/tmp/mplconfig ../ml_env/bin/python -m unittest -v test_integration.py
../ml_env/bin/python service.py
```
