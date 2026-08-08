"""Measure local endpoint latency with Flask's in-process test client."""
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

from app import create_app

PAYLOAD = {"sepal_length": 6.7, "sepal_width": 3.1, "petal_length": 4.7, "petal_width": 1.5}


def main() -> None:
    client = create_app().test_client()
    for _ in range(10):
        assert client.post("/predict", json=PAYLOAD).status_code == 200
    elapsed = []
    last = None
    for _ in range(200):
        start = time.perf_counter()
        last = client.post("/predict", json=PAYLOAD)
        elapsed.append((time.perf_counter() - start) * 1000)
    ordered = sorted(elapsed)
    result = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": f"Python {platform.python_version()}, local Flask test client",
        "requests": len(elapsed),
        "mean_ms": round(statistics.mean(elapsed), 4),
        "median_ms": round(statistics.median(elapsed), 4),
        "p95_ms": round(ordered[int(0.95 * len(ordered)) - 1], 4),
        "max_ms": round(max(elapsed), 4),
        "acceptance_threshold_p95_ms": 100.0,
        "acceptable": ordered[int(0.95 * len(ordered)) - 1] < 100.0,
        "sample_response": last.get_json(),
    }
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(exist_ok=True)
    (out / "latency_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
