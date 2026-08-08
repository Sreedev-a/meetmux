# Submission — Phase 1 Task 20

## Submit

- `app.py`, `test_api.py`, and `benchmark.py`
- The complete `artifacts/` directory
- Generated `outputs/latency_results.json`
- `requirements.txt`, `README.md`, and `WRITTEN_ANSWER.md`

## Verification and screenshots

Run `../ml_env/bin/python -m unittest -v test_api.py` and `../ml_env/bin/python benchmark.py` from this folder. For the live demo, start `app.py`, then capture successful `/health` and `/predict` curl responses. Optionally capture an invalid request showing the structured 422 validation response.
