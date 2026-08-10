"""Generate the reproducible Task 2 dataset, profiles, reports and plots."""

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).parent / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from src.leakage_check import exact_target_copies, suspicious_feature_names, vetted_features
from src.load_data import TARGET, load_dataset, predictors_and_target, save_dataset
from src.profile_features import duplicate_row_count, profile_features
from src.split_data import RANDOM_STATE, split_data, split_summary

ROOT = Path(__file__).resolve().parent


def save_plots(features: pd.DataFrame, target: pd.Series, profile: pd.DataFrame) -> None:
    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)

    counts = target.map({0: "malignant", 1: "benign"}).value_counts().reindex(["malignant", "benign"])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(counts.index, counts.values, color=["#b44b4b", "#4b82b4"])
    ax.bar_label(bars)
    ax.set(title="Class Balance", xlabel="Diagnosis", ylabel="Samples")
    fig.tight_layout(); fig.savefig(output / "class_balance.png", dpi=180); plt.close(fig)

    missing = profile.set_index("feature")["missing_count"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(range(len(missing)), missing.values, color="#5c8f65")
    ax.set(title="Missing Values by Feature (all zero)", xlabel="Feature index", ylabel="Missing values")
    ax.set_xticks(range(len(missing))); ax.set_xticklabels(range(1, len(missing) + 1), fontsize=7)
    fig.tight_layout(); fig.savefig(output / "missing_values.png", dpi=180); plt.close(fig)

    variances = features.var().sort_values(ascending=False).head(10).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(variances.index, variances.values, color="#7868a6")
    ax.set(title="Ten Highest-Variance Raw Features", xlabel="Sample variance (original units)", ylabel="Feature")
    fig.tight_layout(); fig.savefig(output / "feature_summary.png", dpi=180); plt.close(fig)


def main() -> dict[str, object]:
    frame = save_dataset(ROOT / "data/dataset_used.csv")
    features, target = predictors_and_target(frame)
    profile = profile_features(features)
    profile.to_csv(ROOT / "reports/FEATURE_PROFILE.csv", index=False)
    vetted = vetted_features(features, profile, TARGET)
    suspicious = suspicious_feature_names(list(features.columns))
    target_copies = exact_target_copies(features, target)
    splits = split_data(features[vetted], target)
    split_table = split_summary(splits)

    dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy.fit(splits.X_train, splits.y_train)
    prediction = dummy.predict(splits.X_test)
    probability_malignant = dummy.predict_proba(splits.X_test)[:, list(dummy.classes_).index(0)]
    baseline = {
        "malignant_recall": recall_score(splits.y_test, prediction, pos_label=0, zero_division=0),
        "malignant_f1": f1_score(splits.y_test, prediction, pos_label=0, zero_division=0),
        "malignant_precision": precision_score(splits.y_test, prediction, pos_label=0, zero_division=0),
        "roc_auc_malignant": roc_auc_score((splits.y_test == 0).astype(int), probability_malignant),
        "accuracy": accuracy_score(splits.y_test, prediction),
    }
    counts = target.value_counts().sort_index()
    percentages = target.value_counts(normalize=True).sort_index() * 100
    summary = {
        "rows": len(frame), "candidate_features": features.shape[1], "vetted_features": len(vetted),
        "missing_values": int(features.isna().sum().sum()), "duplicate_rows": duplicate_row_count(frame),
        "malignant_count": int(counts[0]), "malignant_percentage": float(percentages[0]),
        "benign_count": int(counts[1]), "benign_percentage": float(percentages[1]),
        "majority_baseline_percentage": float(percentages.max()), "suspicious_names": suspicious,
        "target_copies": target_copies, "split": split_table.to_dict(orient="records"), "baseline": baseline,
        "vetted_feature_names": vetted,
    }
    (ROOT / "outputs/analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    manual = frame.loc[[0, 1, 19, 20, 100, 200, 300, 500], ["mean radius", "mean texture", "mean perimeter", TARGET]].copy()
    manual.insert(0, "sample_id", manual.index)
    manual["label"] = manual[TARGET].map({0: "malignant", 1: "benign"})
    manual.to_csv(ROOT / "reports/manual_label_examples.csv", index=False)

    (ROOT / "reports/FEATURE_PROFILE.md").write_text(
        f"# Feature Profile Summary\n\nAll {features.shape[1]} candidate predictors are numeric measurements computed from digitized fine-needle aspirate images. "
        f"All {len(vetted)} are marked **KEEP**: there are {summary['missing_values']} missing values, no constant columns, and {summary['duplicate_rows']} duplicate complete rows. "
        "Ranges differ substantially, so scale-sensitive models require training-only standardization. Several radius, perimeter and area variants are highly correlated by construction; they remain at this scoping stage because correlation alone is not leakage, but regularization or later redundancy analysis is recommended. Raw variance is unit-dependent and is visualized only as a range diagnostic, not feature importance.\n",
        encoding="utf-8",
    )
    vetted_lines = "\n".join(f"- `{name}`" for name in vetted)
    (ROOT / "reports/LEAKAGE_REPORT.md").write_text(
        "# Leakage Report\n\nTarget leakage is information that would be unavailable at prediction time or directly reveals the outcome, producing unrealistically optimistic evaluation.\n\n"
        f"The `target` column was separated before profiling and splitting. Name screening found {len(suspicious)} suspicious predictor names; exact-copy checks found {len(target_copies)} target copies. "
        "The 30 predictors are image-derived nuclear measurements available for the diagnostic observation, with no post-outcome fields or identifiers. No direct target leakage was identified among the candidate predictor features.\n\n"
        "Splitting occurs before any learned preprocessing. The dataset has no duplicate complete rows, preventing duplicate observations from crossing splits. Future pipelines must fit imputers/scalers only on training data.\n\n## VETTED_FEATURES\n\n" + vetted_lines + "\n",
        encoding="utf-8",
    )
    save_plots(features, target, profile)
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
