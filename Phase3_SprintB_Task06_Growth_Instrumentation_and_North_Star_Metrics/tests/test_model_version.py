from src.ranking_instrumentation import InstrumentedRanker
from tests.conftest import fake_predict


def test_model_version_on_every_result(logger):
    result = InstrumentedRanker(fake_predict, logger).rank(features=[1, 1, 1], request_id="r", session_id="s", actor_id="u")
    assert all(row["model_version"] == "2.0.0" for row in result["results"])


def test_model_failure_uses_explicit_fallback(logger, store):
    result = InstrumentedRanker(fake_predict, logger).rank(features=[1, 1, 1], request_id="r", session_id="s", actor_id="u", force_failure=True)
    assert result["fallback_used"] and result["model_version"] == "fallback-v1"
    assert all(event.fallback_used and event.fallback_reason == "injected_model_failure" for event in store.read_all())
