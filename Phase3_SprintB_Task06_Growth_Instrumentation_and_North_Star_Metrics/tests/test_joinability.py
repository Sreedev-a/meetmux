import pytest

from src.event_store import DuplicateEventError
from src.metrics import validate_joinability
from src.schemas import EventType
from src.trace import reconstruct_lineage


def test_full_outcome_lineage(logger, store, impression):
    logger.log_click(impression.impression_id)
    logger.log_apply(impression.impression_id, "app1")
    logger.log_shortlist(impression.impression_id, "app1", "short1")
    events = store.read_all()
    assert [event.event_type for event in reconstruct_lineage(events, impression.impression_id)] == [EventType.IMPRESSION, EventType.CLICK, EventType.APPLY, EventType.SHORTLIST]
    assert validate_joinability(events)["overall_join_rate"] == 1.0


def test_orphan_outcome_rejected(logger):
    with pytest.raises(ValueError, match="does not exist"): logger.log_click("imp_missing")


def test_duplicate_event_id_rejected(store, impression):
    with pytest.raises(DuplicateEventError): store.append(impression)
