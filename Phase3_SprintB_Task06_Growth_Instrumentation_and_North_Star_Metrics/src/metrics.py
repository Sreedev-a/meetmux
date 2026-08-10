"""Safe funnel, coverage, position, model and joinability metrics."""

from collections import Counter, defaultdict

from .schemas import EventType, RankingEvent


def safe_rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def event_counts(events: list[RankingEvent]) -> dict[str, int]:
    counts = Counter(event.event_type.value for event in events)
    return {kind.value: counts[kind.value] for kind in EventType}


def calculate_funnel(events: list[RankingEvent]) -> dict[str, float | int]:
    counts = event_counts(events)
    return {**counts, "ctr": safe_rate(counts["click"], counts["impression"]), "apply_rate_per_impression": safe_rate(counts["apply"], counts["impression"]), "apply_rate_per_click": safe_rate(counts["apply"], counts["click"]), "shortlist_rate_per_application": safe_rate(counts["shortlist"], counts["apply"]), "shortlist_rate_per_impression": safe_rate(counts["shortlist"], counts["impression"])}


def _group_metrics(events: list[RankingEvent], attribute: str) -> dict[str, dict[str, float | int]]:
    groups: dict[object, list[RankingEvent]] = defaultdict(list)
    for event in events:
        groups[getattr(event, attribute)].append(event)
    result = {}
    for key, rows in sorted(groups.items(), key=lambda pair: str(pair[0])):
        funnel = calculate_funnel(rows)
        result[str(key)] = {"impressions": funnel["impression"], "clicks": funnel["click"], "applies": funnel["apply"], "shortlists": funnel["shortlist"], "ctr": funnel["ctr"], "apply_rate": funnel["apply_rate_per_impression"], "shortlist_rate": funnel["shortlist_rate_per_impression"]}
    return result


def metrics_by_position(events: list[RankingEvent]) -> dict[str, dict[str, float | int]]:
    return _group_metrics(events, "rank_position")


def metrics_by_model_version(events: list[RankingEvent]) -> dict[str, dict[str, float | int]]:
    return _group_metrics(events, "model_version")


def validate_joinability(events: list[RankingEvent]) -> dict[str, object]:
    impressions = {event.impression_id for event in events if event.event_type == EventType.IMPRESSION}
    result: dict[str, object] = {}
    all_orphans: list[str] = []
    for kind in (EventType.CLICK, EventType.APPLY, EventType.SHORTLIST):
        rows = [event for event in events if event.event_type == kind]
        orphans = [event.event_id for event in rows if event.impression_id not in impressions]
        result[f"{kind.value}_total"] = len(rows)
        result[f"{kind.value}_join_rate"] = safe_rate(len(rows) - len(orphans), len(rows)) if rows else 1.0
        result[f"{kind.value}_orphans"] = orphans
        all_orphans.extend(orphans)
    outcome_total = sum(result[f"{kind.value}_total"] for kind in (EventType.CLICK, EventType.APPLY, EventType.SHORTLIST))
    result["overall_join_rate"] = safe_rate(outcome_total - len(all_orphans), outcome_total) if outcome_total else 1.0
    return result


def calculate_logging_coverage(events: list[RankingEvent]) -> dict[str, float | int]:
    impressions = [event for event in events if event.event_type == EventType.IMPRESSION]
    total = len(impressions)
    return {"impressions": total, "position_valid": sum(event.rank_position >= 1 for event in impressions), "position_coverage": safe_rate(sum(event.rank_position >= 1 for event in impressions), total), "model_version_present": sum(bool(event.model_version) for event in impressions), "model_version_coverage": safe_rate(sum(bool(event.model_version) for event in impressions), total), "unique_event_ids": len({event.event_id for event in events}), "total_events": len(events), "schema_validation_rate": 1.0}
