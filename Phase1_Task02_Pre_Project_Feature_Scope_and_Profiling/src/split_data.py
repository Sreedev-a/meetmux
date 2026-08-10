"""Reproducible stratified 70/15/15 train-validation-test split."""

from typing import NamedTuple

import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


class DataSplits(NamedTuple):
    X_train: pd.DataFrame
    X_validation: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_validation: pd.Series
    y_test: pd.Series


def split_data(features: pd.DataFrame, target: pd.Series) -> DataSplits:
    X_train, X_temp, y_train, y_temp = train_test_split(
        features, target, test_size=0.30, random_state=RANDOM_STATE, stratify=target
    )
    X_validation, X_test, y_validation, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=RANDOM_STATE, stratify=y_temp
    )
    return DataSplits(X_train, X_validation, X_test, y_train, y_validation, y_test)


def split_summary(splits: DataSplits) -> pd.DataFrame:
    rows = []
    for name, y in (("train", splits.y_train), ("validation", splits.y_validation), ("test", splits.y_test)):
        counts = y.value_counts().sort_index()
        rows.append({"split": name, "rows": len(y), "malignant": int(counts.get(0, 0)), "benign": int(counts.get(1, 0))})
    return pd.DataFrame(rows)
