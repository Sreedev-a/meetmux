"""Versioned, privacy-minimized ranking event contract."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class EventType(str, Enum):
    IMPRESSION = "impression"
    CLICK = "click"
    APPLY = "apply"
    SHORTLIST = "shortlist"


class RankingEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    event_id: str = Field(min_length=1)
    event_type: EventType
    event_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str = Field(min_length=1)
    ranking_id: str = Field(min_length=1)
    impression_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    actor_id: str = Field(min_length=1)
    item_id: str = Field(min_length=1)
    item_type: str = "job"
    rank_position: int = Field(ge=1)
    score: float | None = None
    model_name: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    feature_version: str = "recommendation-features-v2"
    schema_version: str = "1.0"
    experiment_id: str | None = None
    variant: str | None = None
    application_id: str | None = None
    shortlist_id: str | None = None
    fallback_used: bool = False
    fallback_reason: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_timestamp")
    @classmethod
    def timestamp_must_be_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("event_timestamp must be timezone-aware")
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def validate_lineage(self) -> "RankingEvent":
        if self.event_type in {EventType.APPLY, EventType.SHORTLIST} and not self.application_id:
            raise ValueError("apply and shortlist events require application_id")
        if self.event_type == EventType.SHORTLIST and not self.shortlist_id:
            raise ValueError("shortlist events require shortlist_id")
        if self.fallback_used and not self.fallback_reason:
            raise ValueError("fallback_reason is required when fallback_used is true")
        return self
