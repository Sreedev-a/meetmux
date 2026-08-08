# Phase 1 Task 19 — Application Model Serializing

This task trains a deterministic Iris classifier and serializes preprocessing and model as one versioned `joblib` pipeline. Metadata records lineage, versions, test metrics, and a SHA-256 checksum. Prediction inputs are validated with Pydantic and exposed through a FastAPI stub.

```bash
../ml_env/bin/python train.py
../ml_env/bin/python -m unittest -v test_model.py
../ml_env/bin/uvicorn api:app --host 127.0.0.1 --port 8000
```

Example payload: `{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}`.
