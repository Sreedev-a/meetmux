"""Flask deployment for the serialized Iris pipeline."""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

import joblib
from flask import Flask, jsonify, request
from pydantic import BaseModel, Field, ValidationError

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


class IrisRequest(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)


@lru_cache(maxsize=1)
def load_model():
    manifest = json.loads((ARTIFACTS / "latest.json").read_text())
    model_path = ARTIFACTS / manifest["model"]
    metadata = json.loads((ARTIFACTS / manifest["metadata"]).read_text())
    actual = hashlib.sha256(model_path.read_bytes()).hexdigest()
    if actual != metadata["artifact_sha256"]:
        raise RuntimeError("Model integrity check failed")
    return joblib.load(model_path), metadata


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        try:
            _, metadata = load_model()
            return jsonify(status="ok", model_version=metadata["artifact_version"])
        except Exception:
            return jsonify(status="unavailable"), 503

    @app.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify(error="content_type_must_be_application_json"), 415
        try:
            payload = IrisRequest.model_validate(request.get_json(silent=False))
            model, metadata = load_model()
            row = [[getattr(payload, name) for name in metadata["feature_names"]]]
            prediction = int(model.predict(row)[0])
            probabilities = model.predict_proba(row)[0]
            return jsonify(
                prediction=prediction,
                species=metadata["target_names"][prediction],
                confidence=round(float(probabilities[prediction]), 6),
                model_version=metadata["artifact_version"],
            )
        except ValidationError as exc:
            return jsonify(error="validation_error", details=exc.errors(include_url=False)), 422
        except Exception as exc:
            app.logger.exception("Prediction failed")
            return jsonify(error="prediction_failed", message=str(exc)), 500

    @app.errorhandler(415)
    def unsupported_media(_error):
        return jsonify(error="content_type_must_be_application_json"), 415

    @app.errorhandler(400)
    def malformed_json(_error):
        return jsonify(error="malformed_json"), 400

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
