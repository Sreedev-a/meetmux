from src.ranking_instrumentation import InstrumentedRanker
from src.schemas import RankingEvent
from tests.conftest import fake_predict


def test_persisted_fallback_events_remain_valid(logger, store):
    response = InstrumentedRanker(fake_predict, logger).rank(features=[1, 2, 3], request_id="fail", session_id="s", actor_id="u", force_failure=True)
    assert [row["job_id"] for row in response["results"]] == ["j1", "j2"]
    assert all(RankingEvent.model_validate(event.model_dump()) for event in store.read_all())
