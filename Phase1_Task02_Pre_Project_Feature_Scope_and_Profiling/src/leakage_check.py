"""Conservative target-leakage checks and vetted-feature selection."""

import re

import pandas as pd

SUSPICIOUS_TERMS = re.compile(r"target|label|diagnosis|outcome|result", re.IGNORECASE)


def suspicious_feature_names(columns: list[str]) -> list[str]:
    return [column for column in columns if SUSPICIOUS_TERMS.search(column)]


def exact_target_copies(features: pd.DataFrame, target: pd.Series) -> list[str]:
    return [column for column in features if features[column].reset_index(drop=True).equals(target.reset_index(drop=True))]


def vetted_features(features: pd.DataFrame, profile: pd.DataFrame, target_name: str) -> list[str]:
    if target_name in features.columns:
        raise ValueError("target must be excluded before feature vetting")
    keep = profile.loc[profile["candidate_status"] == "KEEP", "feature"].tolist()
    copied = set(exact_target_copies(features[keep], pd.Series(dtype=float))) if features.empty else set()
    return [name for name in keep if name not in copied]
