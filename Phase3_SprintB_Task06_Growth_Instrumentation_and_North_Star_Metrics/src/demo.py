"""Deterministic controlled driver through the actual instrumented ranking path."""

import importlib.util
import random
from pathlib import Path

from .event_logger import EventLogger
from .event_store import JsonlEventStore
from .ranking_instrumentation import InstrumentedRanker

RANDOM_STATE = 42


def load_existing_predict(repository_root: Path):
    path = repository_root / "Phase3_SprintA_Task05_Reliability_Sign_off_and_Scale_Integration/service.py"
    spec = importlib.util.spec_from_file_location("existing_recommendation_service", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.predict


def run_flow(repository_root: Path, log_path: Path, ranking_requests: int = 150) -> tuple[list, dict]:
    if log_path.exists():
        log_path.unlink()
    store = JsonlEventStore(log_path)
    logger = EventLogger(store)
    ranker = InstrumentedRanker(load_existing_predict(repository_root), logger)
    rng = random.Random(RANDOM_STATE)
    completed_trace = None
    fallback_response = None
    for request_number in range(ranking_requests):
        response = ranker.rank(features=[rng.uniform(0.2, 1.0) for _ in range(3)], request_id=f"runtime_req_{request_number:04d}", session_id=f"session_{request_number // 5:03d}", actor_id=f"student_{request_number % 25:03d}", force_failure=request_number == ranking_requests - 1, experiment_id="ranking_growth_2026_08", variant="control" if request_number % 2 == 0 else "candidate")
        if response["fallback_used"]:
            fallback_response = response
        for result in response["results"]:
            # Controlled action probabilities decrease with rank position to expose position bias.
            if rng.random() < 0.55 / result["rank_position"]:
                logger.log_click(result["impression_id"])
                if rng.random() < 0.48:
                    application_id = f"app_{request_number:04d}_{result['job_id']}"
                    logger.log_apply(result["impression_id"], application_id)
                    if rng.random() < 0.38:
                        logger.log_shortlist(result["impression_id"], application_id, f"short_{request_number:04d}_{result['job_id']}")
                        completed_trace = result["impression_id"]
    assert fallback_response is not None and completed_trace is not None
    return store.read_all(), {"completed_trace": completed_trace, "fallback_response": fallback_response, "ranking_requests": ranking_requests, "simulation": "controlled interaction simulation"}
