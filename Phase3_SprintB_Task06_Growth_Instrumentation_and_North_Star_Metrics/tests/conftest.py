from pathlib import Path

import pytest

from src.event_logger import EventLogger
from src.event_store import JsonlEventStore


def fake_predict(features, force_failure=False):
    if force_failure:
        return {"results": [{"job_id": "j1", "score": None}, {"job_id": "j2", "score": None}], "model_version": "2.0.0", "fallback": True, "reason": "injected_model_failure"}
    return {"results": [{"job_id": "j2", "score": .9}, {"job_id": "j1", "score": .8}, {"job_id": "j3", "score": .7}], "model_version": "2.0.0", "fallback": False}


@pytest.fixture
def store(tmp_path: Path):
    return JsonlEventStore(tmp_path / "events.jsonl")


@pytest.fixture
def logger(store):
    return EventLogger(store)


@pytest.fixture
def impression(logger):
    return logger.log_impression(request_id="req1", ranking_id="rank1", session_id="session1", actor_id="student1", item_id="job1", rank_position=1, score=.9, model_name="ranker", model_version="v1")
