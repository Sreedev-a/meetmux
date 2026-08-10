from src.ranking_instrumentation import InstrumentedRanker
from src.trace import reconstruct_ranked_list
from tests.conftest import fake_predict


def test_every_result_is_instrumented_without_order_change(logger, store):
    response = InstrumentedRanker(fake_predict, logger).rank(features=[1, 2, 3], request_id="req", session_id="s", actor_id="u")
    assert [row["job_id"] for row in response["results"]] == ["j2", "j1", "j3"]
    assert [row["rank_position"] for row in response["results"]] == [1, 2, 3]
    assert all(row["impression_id"] for row in response["results"])
    rebuilt = reconstruct_ranked_list(store.read_all(), response["ranking_id"])
    assert [event.item_id for event in rebuilt] == ["j2", "j1", "j3"]


def test_requests_do_not_mix_ranking_ids(logger):
    ranker = InstrumentedRanker(fake_predict, logger)
    first = ranker.rank(features=[1, 2, 3], request_id="r1", session_id="s", actor_id="u")
    second = ranker.rank(features=[1, 2, 3], request_id="r2", session_id="s", actor_id="u")
    assert first["ranking_id"] != second["ranking_id"]
    assert len({row["ranking_id"] for row in first["results"]}) == 1
