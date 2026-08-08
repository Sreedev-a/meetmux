# Submission — Phase 1 Task 19

## Files to submit

- `train.py`, `predict.py`, and `api.py`
- `artifacts/iris_pipeline_v1.0.0.joblib`
- `artifacts/iris_pipeline_v1.0.0.metadata.json` and `artifacts/latest.json`
- `test_model.py`, `requirements.txt`, `README.md`, and `WRITTEN_ANSWER.md`

## Reproduce and verify

```bash
../ml_env/bin/python train.py
../ml_env/bin/python -m unittest -v test_model.py
```

Expected result: four passing tests and metadata containing real held-out metrics. For a demo, start Uvicorn as shown in the README, capture `/health`, then POST the example payload to `/predict` and capture the JSON response.
