"""Single construction path for impressions and lineage-preserving outcomes."""

from uuid import uuid4

from .event_store import JsonlEventStore
from .schemas import EventType, RankingEvent


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class EventLogger:
    def __init__(self, store: JsonlEventStore):
        self.store = store

    def log_impression(self, **fields) -> RankingEvent:
        event = RankingEvent(event_id=new_id("evt"), event_type=EventType.IMPRESSION, impression_id=new_id("imp"), **fields)
        self.store.append(event)
        return event

    def log_outcome(self, event_type: EventType, impression_id: str, *, application_id: str | None = None, shortlist_id: str | None = None, metadata: dict | None = None) -> RankingEvent:
        if event_type == EventType.IMPRESSION:
            raise ValueError("use log_impression for impressions")
        source = self.store.find_impression(impression_id)
        if source is None:
            raise ValueError("originating impression does not exist")
        payload = source.model_dump(exclude={"event_id", "event_type", "event_timestamp", "score", "application_id", "shortlist_id", "metadata"})
        event = RankingEvent(event_id=new_id("evt"), event_type=event_type, score=None, application_id=application_id, shortlist_id=shortlist_id, metadata=metadata or {}, **payload)
        self.store.append(event)
        return event

    def log_click(self, impression_id: str) -> RankingEvent:
        return self.log_outcome(EventType.CLICK, impression_id)

    def log_apply(self, impression_id: str, application_id: str) -> RankingEvent:
        return self.log_outcome(EventType.APPLY, impression_id, application_id=application_id)

    def log_shortlist(self, impression_id: str, application_id: str, shortlist_id: str) -> RankingEvent:
        return self.log_outcome(EventType.SHORTLIST, impression_id, application_id=application_id, shortlist_id=shortlist_id)
