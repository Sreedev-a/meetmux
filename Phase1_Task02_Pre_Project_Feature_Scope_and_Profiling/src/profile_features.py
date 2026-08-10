"""Pandas-based feature inventory and data-quality profiling."""

import numpy as np
import pandas as pd


PROFILE_COLUMNS = [
    "feature", "dtype", "non_null_count", "missing_count", "missing_percentage",
    "unique_count", "unique_percentage", "min", "max", "mean", "median", "std",
    "candidate_status", "reason",
]


def profile_features(features: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    total = len(features)
    for name in features.columns:
        series = features[name]
        numeric = pd.api.types.is_numeric_dtype(series)
        unique = int(series.nunique(dropna=True))
        status, reason = "KEEP", "valid pre-diagnosis numeric measurement"
        if unique <= 1:
            status, reason = "DROP", "constant feature"
        elif name.lower() in {"id", "sample_id", "patient_id"} or name.lower().endswith("_id"):
            status, reason = "DROP", "identifier, not a clinical predictor"
        rows.append({
            "feature": name,
            "dtype": str(series.dtype),
            "non_null_count": int(series.notna().sum()),
            "missing_count": int(series.isna().sum()),
            "missing_percentage": round(float(series.isna().mean() * 100), 4),
            "unique_count": unique,
            "unique_percentage": round(float(unique / total * 100), 4),
            "min": float(series.min()) if numeric else np.nan,
            "max": float(series.max()) if numeric else np.nan,
            "mean": float(series.mean()) if numeric else np.nan,
            "median": float(series.median()) if numeric else np.nan,
            "std": float(series.std()) if numeric else np.nan,
            "candidate_status": status,
            "reason": reason,
        })
    return pd.DataFrame(rows, columns=PROFILE_COLUMNS)


def duplicate_row_count(frame: pd.DataFrame) -> int:
    return int(frame.duplicated().sum())
