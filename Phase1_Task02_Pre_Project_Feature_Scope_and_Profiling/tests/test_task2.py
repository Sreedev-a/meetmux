import pandas as pd

from src.leakage_check import vetted_features
from src.load_data import TARGET, load_dataset, predictors_and_target
from src.profile_features import profile_features
from src.split_data import split_data


def test_data_loads_with_expected_binary_target() -> None:
    frame = load_dataset()
    assert frame.shape == (569, 31)
    assert TARGET in frame
    assert set(frame[TARGET]) == {0, 1}


def test_profile_is_complete_and_non_mutating() -> None:
    frame = load_dataset()
    features, _ = predictors_and_target(frame)
    original = features.copy(deep=True)
    profile = profile_features(features)
    assert len(profile) == features.shape[1]
    assert set(profile["feature"]) == set(features.columns)
    pd.testing.assert_frame_equal(features, original)


def test_target_is_excluded_from_vetted_features() -> None:
    features, _ = predictors_and_target(load_dataset())
    vetted = vetted_features(features, profile_features(features), TARGET)
    assert TARGET not in features
    assert TARGET not in vetted
    assert len(vetted) == 30


def test_class_counts_sum_to_dataset_size() -> None:
    frame = load_dataset()
    assert int(frame[TARGET].value_counts().sum()) == len(frame)


def test_split_is_disjoint_complete_and_reproducible() -> None:
    features, target = predictors_and_target(load_dataset())
    first = split_data(features, target)
    second = split_data(features, target)
    indices = [set(first.X_train.index), set(first.X_validation.index), set(first.X_test.index)]
    assert sum(map(len, indices)) == len(features)
    assert not (indices[0] & indices[1] or indices[0] & indices[2] or indices[1] & indices[2])
    assert first.X_train.index.tolist() == second.X_train.index.tolist()
    assert TARGET not in first.X_train.columns
