"""Minimal FastAPI serving stub for Task 19."""
from fastapi import FastAPI, HTTPException

from predict import IrisFeatures, load_bundle, predict_one

app = FastAPI(title="PlaceMux Serialized Model", version="1.0.0")


@app.get("/health")
def health() -> dict:
    try:
        _, metadata = load_bundle()
        return {"status": "ok", "model_version": metadata["artifact_version"]}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict")
def predict(payload: IrisFeatures) -> dict:
    return predict_one(payload)
