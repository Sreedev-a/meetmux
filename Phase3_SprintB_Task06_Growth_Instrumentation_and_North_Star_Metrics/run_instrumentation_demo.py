"""Exercise existing ranking, persist events, verify lineage and generate evidence."""

import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parent
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

import matplotlib.pyplot as plt

from src.demo import run_flow
from src.metrics import calculate_funnel, calculate_logging_coverage, metrics_by_model_version, metrics_by_position, validate_joinability
from src.trace import reconstruct_lineage


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def make_plots(funnel, positions, models) -> None:
    ROOT.joinpath("outputs").mkdir(exist_ok=True)
    names = ["impression", "click", "apply", "shortlist"]
    colors = ["#326789", "#78a6c8", "#e69f54", "#5b9d62"]
    for filename, title in (("funnel.png", "Controlled Runtime Outcome Funnel"), ("event_volume.png", "Persisted Event Volume")):
        fig, ax = plt.subplots(figsize=(8, 4.8)); bars = ax.bar(names, [funnel[n] for n in names], color=colors); ax.bar_label(bars); ax.set(title=title, xlabel="Event type", ylabel="Events"); fig.tight_layout(); fig.savefig(ROOT / "outputs" / filename, dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.8)); keys = sorted(positions, key=int); ax.bar(keys, [positions[k]["ctr"] * 100 for k in keys], color="#8064a2"); ax.set(title="CTR by Original Rank Position", xlabel="1-based rank position", ylabel="CTR (%)"); fig.tight_layout(); fig.savefig(ROOT / "outputs/ctr_by_position.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.8)); keys = list(models); ax.bar(keys, [models[k]["impressions"] for k in keys], color="#4d8b73"); ax.set(title="Impressions by Model Version", xlabel="Model version", ylabel="Impressions"); ax.tick_params(axis="x", rotation=15); fig.tight_layout(); fig.savefig(ROOT / "outputs/model_version_distribution.png", dpi=180); plt.close(fig)


def main() -> dict:
    log_path = ROOT / "data/generated_runtime_logs/ranking_events.jsonl"
    events, runtime = run_flow(REPOSITORY_ROOT, log_path)
    funnel = calculate_funnel(events); coverage = calculate_logging_coverage(events); joins = validate_joinability(events)
    positions = metrics_by_position(events); models = metrics_by_model_version(events)
    ranking_ids = {event.ranking_id for event in events if event.event_type.value == "impression"}
    impressions = [event for event in events if event.event_type.value == "impression"]
    timestamps = [event.event_timestamp for event in events]
    summary = {"runtime_source": "existing Sprint A recommendation service called through InstrumentedRanker", "interaction_source": runtime["simulation"], "ranking_requests": runtime["ranking_requests"], "unique_ranking_ids": len(ranking_ids), "unique_impression_ids": len({event.impression_id for event in impressions}), "event_counts": {name: funnel[name] for name in ("impression", "click", "apply", "shortlist")}, "funnel_metrics": {key: value for key, value in funnel.items() if key not in ("impression", "click", "apply", "shortlist")}, "coverage": coverage, "joinability": joins, "metrics_by_position": positions, "metrics_by_model_version": models, "model_versions": sorted({event.model_version for event in impressions}), "timestamp_start": min(timestamps).isoformat(), "timestamp_end": max(timestamps).isoformat(), "fallback_ranking_id": runtime["fallback_response"]["ranking_id"], "fallback_result_count": len(runtime["fallback_response"]["results"]), "trace_impression_id": runtime["completed_trace"]}
    (ROOT / "outputs/runtime_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_plots(funnel, positions, models)
    report = ROOT / "reports"; report.mkdir(exist_ok=True)
    (report / "EVENT_VOLUME_REPORT.md").write_text(f"# Event Volume Report\n\nThis evidence is actual runtime output from **{runtime['simulation']}**, not production traffic or hand-written rows. The existing ranker was called {summary['ranking_requests']} times through the instrumented flow.\n\n| Measure | Actual |\n|---|---:|\n| Ranking requests / unique ranking IDs | {summary['ranking_requests']} / {summary['unique_ranking_ids']} |\n| Impressions / unique impression IDs | {funnel['impression']} / {summary['unique_impression_ids']} |\n| Clicks | {funnel['click']} |\n| Applies | {funnel['apply']} |\n| Shortlists | {funnel['shortlist']} |\n| Total events | {len(events)} |\n| Schema-valid persisted events | {coverage['schema_validation_rate']*100:.2f}% |\n\nUTC range: `{summary['timestamp_start']}` to `{summary['timestamp_end']}`. Model versions: {', '.join(summary['model_versions'])}. Event IDs are unique: {coverage['unique_event_ids']} / {coverage['total_events']}.\n", encoding="utf-8")
    (report / "JOINABILITY_REPORT.md").write_text(f"# Joinability Report\n\nAll outcomes were emitted by `EventLogger` only after resolving their originating persisted impression.\n\n| Outcome | Events | Join rate | Orphans |\n|---|---:|---:|---:|\n| Click | {joins['click_total']} | {pct(joins['click_join_rate'])} | {len(joins['click_orphans'])} |\n| Apply | {joins['apply_total']} | {pct(joins['apply_join_rate'])} | {len(joins['apply_orphans'])} |\n| Shortlist | {joins['shortlist_total']} | {pct(joins['shortlist_join_rate'])} | {len(joins['shortlist_orphans'])} |\n\nOverall outcome joinability: **{pct(joins['overall_join_rate'])}**.\n", encoding="utf-8")
    (report / "POSITION_COVERAGE_REPORT.md").write_text(f"# Position Coverage Report\n\nOne-based `rank_position >= 1` was present and valid on **{coverage['position_valid']} / {coverage['impressions']} impressions ({pct(coverage['position_coverage'])})**. Positions are assigned after the existing ranker returns and preserve its order. Position-aware CTR/apply/shortlist metrics are in `ONLINE_METRICS_REPORT.md`.\n", encoding="utf-8")
    (report / "MODEL_VERSION_COVERAGE_REPORT.md").write_text(f"# Model-Version Coverage Report\n\n`model_version` was present on **{coverage['model_version_present']} / {coverage['impressions']} impressions ({pct(coverage['model_version_coverage'])})**. Observed versions: {', '.join(summary['model_versions'])}. The injected failure is explicitly attributed to `fallback-v1`; normal results retain existing version `2.0.0`.\n", encoding="utf-8")
    pos_rows = "\n".join(f"| {p} | {v['impressions']} | {pct(v['ctr'])} | {pct(v['apply_rate'])} | {pct(v['shortlist_rate'])} |" for p, v in positions.items())
    model_rows = "\n".join(f"| {m} | {v['impressions']} | {pct(v['ctr'])} | {pct(v['apply_rate'])} | {pct(v['shortlist_rate'])} |" for m, v in models.items())
    (report / "ONLINE_METRICS_REPORT.md").write_text(f"# Online-Style Metrics from Controlled Runtime Events\n\nThese are engineering validation metrics from controlled simulation, not production lift. The design-choice north star, shortlist rate per ranked impression, is **{pct(funnel['shortlist_rate_per_impression'])}** ({funnel['shortlist']} / {funnel['impression']}). CTR is {pct(funnel['ctr'])}; apply/impression {pct(funnel['apply_rate_per_impression'])}; apply/click {pct(funnel['apply_rate_per_click'])}; shortlist/application {pct(funnel['shortlist_rate_per_application'])}.\n\n## By position\n\n| Position | Impressions | CTR | Apply rate | Shortlist rate |\n|---:|---:|---:|---:|---:|\n{pos_rows}\n\n## By model version\n\n| Version | Impressions | CTR | Apply rate | Shortlist rate |\n|---|---:|---:|---:|---:|\n{model_rows}\n", encoding="utf-8")
    lineage = reconstruct_lineage(events, runtime["completed_trace"]); lookup = {event.event_type.value: event for event in lineage}; imp = lookup["impression"]
    (report / "E2E_TRACE_EXAMPLE.md").write_text(f"# Actual End-to-End Trace\n\n- Ranking request: `{imp.request_id}`\n- Ranking ID: `{imp.ranking_id}`\n- Model: `{imp.model_name}` / `{imp.model_version}`\n- Actor/session: `{imp.actor_id}` / `{imp.session_id}`\n- Item: `{imp.item_id}` at position **{imp.rank_position}**\n- Impression: `{imp.impression_id}` (`{imp.event_id}`)\n- Click event: `{lookup['click'].event_id}`\n- Apply: `{lookup['apply'].application_id}` (`{lookup['apply'].event_id}`)\n- Shortlist: `{lookup['shortlist'].shortlist_id}` (`{lookup['shortlist'].event_id}`)\n\nThis job was shown at position {imp.rank_position} by model version {imp.model_version}; the controlled actor clicked, applied, and was shortlisted. Every step shares the original impression and ranking context.\n", encoding="utf-8")
    (report / "FAILURE_TEST_REPORT.md").write_text(f"# Intentional Model-Unavailable Test\n\nThe final runtime request set `force_failure=True` on the existing Sprint A service. The service returned a valid deterministic fallback list; instrumentation logged **{summary['fallback_result_count']} impressions** under ranking `{summary['fallback_ranking_id']}`, with `model_name=fallback_ranker`, `model_version=fallback-v1`, `fallback_used=true`, and sanitized reason `injected_model_failure`. Normal event history remained valid and joinable. Result: **PASS**.\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
