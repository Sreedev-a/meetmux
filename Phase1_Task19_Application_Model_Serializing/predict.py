"""Validated loading and prediction for the versioned model."""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

import joblib
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def load_bundle():
    latest = json.loads((ARTIFACTS / "latest.json").read_text(encoding="utf-8"))
    model_path = ARTIFACTS / latest["model"]
    metadata = json.loads((ARTIFACTS / latest["metadata"]).read_text(encoding="utf-8"))
    if _digest(model_path) != metadata["artifact_sha256"]:
        raise RuntimeError("Artifact checksum does not match metadata")
    return joblib.load(model_path), metadata


def predict_one(features: IrisFeatures) -> dict:
    model, metadata = load_bundle()
    row = [[getattr(features, name) for name in metadata["feature_names"]]]
    probabilities = model.predict_proba(row)[0]
    class_id = int(model.predict(row)[0])
    return {
        "class_id": class_id,
        "class_name": metadata["target_names"][class_id],
        "confidence": round(float(probabilities[class_id]), 6),
        "model_version": metadata["artifact_version"],
    }
