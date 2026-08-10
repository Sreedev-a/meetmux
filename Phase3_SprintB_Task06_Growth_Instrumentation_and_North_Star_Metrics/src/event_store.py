"""Append-only JSONL event store with event-id idempotency."""

import json
from pathlib import Path

from .schemas import RankingEvent


class DuplicateEventError(ValueError):
    pass


class JsonlEventStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._event_ids = {event.event_id for event in self.read_all()} if path.exists() else set()

    def append(self, event: RankingEvent) -> None:
        if event.event_id in self._event_ids:
            raise DuplicateEventError(f"duplicate event_id: {event.event_id}")
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(event.model_dump_json() + "\n")
        self._event_ids.add(event.event_id)

    def read_all(self) -> list[RankingEvent]:
        if not self.path.exists():
            return []
        return [RankingEvent.model_validate_json(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def find_impression(self, impression_id: str) -> RankingEvent | None:
        return next((event for event in self.read_all() if event.event_type.value == "impression" and event.impression_id == impression_id), None)
