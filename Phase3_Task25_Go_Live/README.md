# Phase 3 Task 25 — Go-Live

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/mplconfig ../ml_env/bin/python monitor.py
MPLCONFIGDIR=/private/tmp/mplconfig ../ml_env/bin/python -m unittest -v test_monitor.py
```

This is a deployable local monitoring proof with deliberate failure injection. See `BLOCKED.md` for the production-only hand-off.
