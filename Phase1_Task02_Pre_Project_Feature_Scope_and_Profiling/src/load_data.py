"""Load the reproducible real-data demonstration without network access."""

from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer

TARGET = "target"
DATASET_NAME = "scikit-learn Wisconsin Breast Cancer dataset"


def load_dataset() -> pd.DataFrame:
    """Return 569 diagnostic samples; target 0=malignant and 1=benign."""
    bunch = load_breast_cancer(as_frame=True)
    frame = bunch.frame.copy()
    frame.index.name = "sample_id"
    return frame


def save_dataset(path: Path) -> pd.DataFrame:
    frame = load_dataset()
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=True)
    return frame


def predictors_and_target(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    if TARGET not in frame:
        raise ValueError(f"required target column {TARGET!r} is missing")
    return frame.drop(columns=TARGET).copy(), frame[TARGET].copy()
