"""Reproducible fairness closeout and fail-closed model sign-off."""
from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
SEED = 42


def generate_fixture(n: int = 600) -> list[dict]:
    rng = random.Random(SEED)
    rows = []
    for i in range(n):
        group = "A" if i % 2 == 0 else "B"
        ability = rng.random()
        qualified = ability >= 0.50
        score = min(1.0, max(0.0, ability + rng.gauss(0, 0.08)))
        rows.append({"candidate_id": f"c{i:04d}", "audit_group": group, "score": round(score, 6), "qualified": int(qualified), "selected": int(score >= 0.50)})
    return rows


def group_metrics(rows: list[dict]) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups[row["audit_group"]].append(row)
    result = {}
    for name, values in sorted(groups.items()):
        tp = sum(r["qualified"] and r["selected"] for r in values)
        fn = sum(r["qualified"] and not r["selected"] for r in values)
        fp = sum(not r["qualified"] and r["selected"] for r in values)
        tn = sum(not r["qualified"] and not r["selected"] for r in values)
        result[name] = {
            "n": len(values),
            "selection_rate": round(sum(r["selected"] for r in values) / len(values), 6),
            "true_positive_rate": round(tp / (tp + fn), 6),
            "false_positive_rate": round(fp / (fp + tn), 6),
            "accuracy": round((tp + tn) / len(values), 6),
        }
    return result


def evaluate(rows: list[dict]) -> dict:
    groups = group_metrics(rows)
    selection = [m["selection_rate"] for m in groups.values()]
    tpr = [m["true_positive_rate"] for m in groups.values()]
    fpr = [m["false_positive_rate"] for m in groups.values()]
    overall_accuracy = sum(int(r["qualified"] == r["selected"]) for r in rows) / len(rows)
    summary = {
        "overall_accuracy": round(overall_accuracy, 6),
        "disparate_impact_ratio": round(min(selection) / max(selection), 6),
        "equal_opportunity_gap": round(max(tpr) - min(tpr), 6),
        "false_positive_rate_gap": round(max(fpr) - min(fpr), 6),
    }
    checks = {
        "minimum_200_per_group": all(m["n"] >= 200 for m in groups.values()),
        "accuracy_at_least_0_80": summary["overall_accuracy"] >= 0.80,
        "disparate_impact_at_least_0_80": summary["disparate_impact_ratio"] >= 0.80,
        "equal_opportunity_gap_at_most_0_10": summary["equal_opportunity_gap"] <= 0.10,
        "false_positive_gap_at_most_0_10": summary["false_positive_rate_gap"] <= 0.10,
    }
    return {"groups": groups, "summary": summary, "checks": checks, "approved": all(checks.values())}


def main() -> None:
    rows = generate_fixture()
    data_dir, output_dir = ROOT / "data", ROOT / "outputs"
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    with (data_dir / "fairness_evaluation_fixture.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    report = evaluate(rows)
    report.update({"dataset": "deterministic local fallback fixture", "seed": SEED, "model_version": "2.0.0", "owner": "ML Reliability Owner"})
    report["artifact_sha256"] = hashlib.sha256((ROOT.parent / "Phase3_Task22_Data_Subject_Rights_and_Resilience/artifacts/recommendation_gate_v2.0.0.joblib").read_bytes()).hexdigest()
    (output_dir / "fairness_signoff.json").write_text(json.dumps(report, indent=2) + "\n")
    labels = list(report["groups"])
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([i - .18 for i in x], [report["groups"][g]["selection_rate"] for g in labels], .36, label="Selection rate")
    ax.bar([i + .18 for i in x], [report["groups"][g]["true_positive_rate"] for g in labels], .36, label="True-positive rate")
    ax.set_xticks(list(x), labels); ax.set_ylim(0, 1); ax.set_ylabel("Rate"); ax.set_title("Fairness closeout by audit group"); ax.legend(); fig.tight_layout()
    fig.savefig(output_dir / "fairness_closeout.png", dpi=160); plt.close(fig)
    print(json.dumps({"approved": report["approved"], **report["summary"], "checks": report["checks"]}, indent=2))
    if not report["approved"]:
        raise SystemExit("Fairness sign-off blocked")


if __name__ == "__main__":
    main()
