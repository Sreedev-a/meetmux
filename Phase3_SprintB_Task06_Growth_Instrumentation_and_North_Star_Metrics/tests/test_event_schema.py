from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.schemas import EventType, RankingEvent


def payload(kind="impression"):
    return dict(event_id="evt1", event_type=kind, event_timestamp=datetime.now(timezone.utc), request_id="req1", ranking_id="rank1", impression_id="imp1", session_id="s1", actor_id="u1", item_id="j1", rank_position=1, model_name="ranker", model_version="v1")


@pytest.mark.parametrize("kind", ["impression", "click"])
def test_impression_and_click_validate(kind):
    assert RankingEvent(**payload(kind)).event_type.value == kind


def test_apply_and_shortlist_validate():
    assert RankingEvent(**payload("apply"), application_id="app1").event_type == EventType.APPLY
    assert RankingEvent(**payload("shortlist"), application_id="app1", shortlist_id="short1").event_type == EventType.SHORTLIST


@pytest.mark.parametrize("change", [{"event_type": "view"}, {"rank_position": 0}, {"model_version": ""}, {"impression_id": ""}, {"event_timestamp": datetime.now()}])
def test_invalid_contract_rejected(change):
    values = payload(); values.update(change)
    with pytest.raises(ValidationError): RankingEvent(**values)


def test_outcome_specific_linkage_rejected():
    with pytest.raises(ValidationError): RankingEvent(**payload("apply"))
    with pytest.raises(ValidationError): RankingEvent(**payload("shortlist"), application_id="app1")
