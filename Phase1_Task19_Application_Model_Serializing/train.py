"""Train and serialize a versioned Iris classification pipeline."""
from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.datasets import load_iris
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
VERSION = "1.0.0"
SEED = 42
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    np.random.seed(SEED)
    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=SEED, stratify=data.target
    )
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=SEED)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 6),
        "macro_f1": round(float(f1_score(y_test, predictions, average="macro")), 6),
        "test_samples": int(len(y_test)),
    }

    ARTIFACTS.mkdir(exist_ok=True)
    model_path = ARTIFACTS / f"iris_pipeline_v{VERSION}.joblib"
    metadata_path = ARTIFACTS / f"iris_pipeline_v{VERSION}.metadata.json"
    joblib.dump(pipeline, model_path)
    metadata = {
        "artifact_version": VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": "sklearn.datasets.load_iris",
        "dataset_samples": int(data.data.shape[0]),
        "feature_names": FEATURES,
        "target_names": data.target_names.tolist(),
        "random_seed": SEED,
        "split": {"test_size": 0.25, "stratified": True},
        "metrics": metrics,
        "libraries": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scikit_learn": sklearn.__version__,
            "joblib": joblib.__version__,
        },
    }
    metadata["artifact_sha256"] = sha256(model_path)
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (ARTIFACTS / "latest.json").write_text(
        json.dumps({"version": VERSION, "model": model_path.name, "metadata": metadata_path.name}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
