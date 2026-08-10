"""Non-order-changing instrumentation adapter for an existing ranker response."""

from collections.abc import Callable
from uuid import uuid4

from .event_logger import EventLogger


class InstrumentedRanker:
    def __init__(self, predict: Callable[..., dict], logger: EventLogger):
        self.predict = predict
        self.logger = logger

    def rank(self, *, features: list[float], request_id: str, session_id: str, actor_id: str, force_failure: bool = False, experiment_id: str | None = None, variant: str | None = None) -> dict:
        raw = self.predict(features, force_failure=force_failure)
        ranking_id = f"rank_{uuid4().hex}"
        fallback = bool(raw.get("fallback"))
        model_name = "fallback_ranker" if fallback else "recommendation_gate"
        model_version = "fallback-v1" if fallback else str(raw["model_version"])
        reason = raw.get("reason") if fallback else None
        results = []
        for position, result in enumerate(raw["results"], start=1):
            impression = self.logger.log_impression(
                request_id=request_id, ranking_id=ranking_id, session_id=session_id, actor_id=actor_id,
                item_id=result["job_id"], rank_position=position, score=result.get("score"),
                model_name=model_name, model_version=model_version, experiment_id=experiment_id,
                variant=variant, fallback_used=fallback, fallback_reason=reason,
                context={"ranking_direction": "jobs_for_student"},
            )
            results.append({**result, "ranking_id": ranking_id, "impression_id": impression.impression_id, "rank_position": position, "model_name": model_name, "model_version": model_version, "fallback_used": fallback})
        return {"request_id": request_id, "ranking_id": ranking_id, "results": results, "model_name": model_name, "model_version": model_version, "fallback_used": fallback, "fallback_reason": reason}
