"""Model-service monitoring evaluator with synthetic failure injection."""
from __future__ import annotations

import csv
import json
import math
import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
SLO = {"availability": 0.995, "p95_latency_ms": 100.0, "min_accuracy": 0.80, "min_score_stddev": 0.03}


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, math.ceil(q * len(ordered)) - 1)]


def summarize(rows: list[dict]) -> dict:
    latency = [float(r["latency_ms"]) for r in rows]
    scores = [float(r["score"]) for r in rows if int(r["success"])]
    labeled = [r for r in rows if r["correct"] != ""]
    metrics = {
        "requests": len(rows),
        "availability": round(sum(int(r["success"]) for r in rows) / len(rows), 6),
        "p95_latency_ms": round(percentile(latency, .95), 4),
        "accuracy": round(sum(int(r["correct"]) for r in labeled) / len(labeled), 6),
        "score_stddev": round(statistics.pstdev(scores), 6),
    }
    alerts = []
    if metrics["availability"] < SLO["availability"]: alerts.append("PAGE_AVAILABILITY")
    if metrics["p95_latency_ms"] > SLO["p95_latency_ms"]: alerts.append("PAGE_LATENCY")
    if metrics["accuracy"] < SLO["min_accuracy"]: alerts.append("PAGE_QUALITY")
    if metrics["score_stddev"] < SLO["min_score_stddev"]: alerts.append("PAGE_DEGENERATE_SCORES")
    return {"metrics": metrics, "alerts": alerts, "healthy": not alerts}


def generate_logs() -> list[dict]:
    rng = random.Random(25)
    rows = []
    for window in ("normal", "injected_failure"):
        for i in range(200):
            failure = window == "injected_failure" and i < 12
            rows.append({
                "window": window,
                "request_id": f"{window[:1]}-{i:04d}",
                "latency_ms": round((rng.uniform(12, 35) if window == "normal" else rng.uniform(80, 180)), 4),
                "success": int(not failure),
                "score": round(rng.uniform(.2, .95), 5) if window == "normal" else .5,
                "correct": int(rng.random() < (.92 if window == "normal" else .65)),
                "model_version": "2.0.0",
            })
    return rows


def main() -> None:
    rows = generate_logs()
    data_dir, out_dir = ROOT / "data", ROOT / "outputs"
    data_dir.mkdir(exist_ok=True); out_dir.mkdir(exist_ok=True)
    with (data_dir / "monitoring_fixture.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    reports = {window: summarize([r for r in rows if r["window"] == window]) for window in ("normal", "injected_failure")}
    result = {"environment": "local deterministic fallback; not production", "slo": SLO, "windows": reports, "failure_path_verified": bool(reports["injected_failure"]["alerts"])}
    (out_dir / "monitoring_report.json").write_text(json.dumps(result, indent=2) + "\n")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(reports.keys(), [x["metrics"]["p95_latency_ms"] for x in reports.values()], color=["#2e8b57", "#b22222"])
    ax.axhline(SLO["p95_latency_ms"], color="black", linestyle="--", label="p95 SLO"); ax.set_ylabel("p95 latency (ms)"); ax.legend(); fig.tight_layout()
    fig.savefig(out_dir / "monitoring_latency.png", dpi=160); plt.close(fig)
    print(json.dumps(result, indent=2))
    if reports["normal"]["alerts"] or not result["failure_path_verified"]:
        raise SystemExit("Monitoring verification failed")


if __name__ == "__main__":
    main()
