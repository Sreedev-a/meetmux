# Phase 1 Task 20 — End-to-End Pipelines & Deployment

This Flask service loads a checksum-verified, versioned preprocessing-and-model pipeline. It provides validated live predictions, health reporting, structured error handling, and a measured latency benchmark.

```bash
../ml_env/bin/python -m unittest -v test_api.py
../ml_env/bin/python benchmark.py
../ml_env/bin/python app.py
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```
