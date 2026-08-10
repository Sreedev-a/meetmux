"""Reconstruct event lineage from a persisted stream."""

from .schemas import RankingEvent


def reconstruct_lineage(events: list[RankingEvent], impression_id: str) -> list[RankingEvent]:
    return sorted((event for event in events if event.impression_id == impression_id), key=lambda event: event.event_timestamp)


def reconstruct_ranked_list(events: list[RankingEvent], ranking_id: str) -> list[RankingEvent]:
    return sorted((event for event in events if event.ranking_id == ranking_id and event.event_type.value == "impression"), key=lambda event: event.rank_position)
