# Phase 3 Sprint B Task 6 — Growth Instrumentation & North-Star Metrics

## Objective

Make PlaceMux ranked recommendations observable and learnable by recording exactly what was shown, its order/model context, and subsequent click, apply and shortlist outcomes.

## Official Deliverables

- Validated impression/click/apply/shortlist schema
- Position and model-version metadata on every ranked result
- Verified, joinable end-to-end runtime flow at meaningful local volume

## Existing Baseline

Phase 2 contains recommendation/ranking and held-out offline evaluation; Sprint A contains a callable versioned service with deterministic fallback. Inspection found no persisted ranked-impression/outcome lineage or production event stream. Existing fixtures were not presented as production logs.

## Architecture

```text
Existing ranker → InstrumentedRanker → ranked response + impressions → JSONL
                                              impression_id ↓
                                      click → apply → shortlist
```

Instrumentation only decorates returned order. Pydantic validates the v1 envelope and `JsonlEventStore` rejects duplicate event IDs.

## Event Schema

All four event types carry UTC time, request/ranking/impression IDs, actor/item IDs, one-based position, model/feature/schema versions, experiment context and fallback state. Apply/shortlist require domain IDs. Details and examples are in `docs/EVENT_SCHEMA.md`.

## Ranking IDs and Impression IDs

One `ranking_id` identifies a complete response; each displayed result has a unique `impression_id`. Outcomes join on impression rather than item ID, so repeated item exposure remains distinguishable.

## Position Logging

Positions start at 1 and preserve existing service order. Executed coverage was **599/599 (100%)**.

## Model-Version Logging

Every impression records the actual producer. Normal results use existing `2.0.0`; injected degradation uses explicit `fallback-v1`. Coverage was **599/599 (100%)**.

## Outcome Joinability

The logger resolves an originating persisted impression before accepting an outcome and copies original context. All 169 clicks, 84 applies and 32 shortlists joined successfully (285/285, 100%).

## Event Storage

`data/generated_runtime_logs/ranking_events.jsonl` is append-only, validated and analyst-readable. The demo recreates it deterministically in action decisions; UUIDs/timestamps are intentionally runtime-generated.

## North-Star Metric

The design-choice north star is qualified shortlist rate per ranked impression: **32/599 = 5.34%** in the controlled run. This validates computation, not production performance.

## Guardrail Metrics

CTR, apply rates, ranking quality, latency/availability, fallback/no-result rates, position/model/schema completeness, duplicates, orphan outcomes and fairness prevent click-only optimization.

## End-to-End Flow and Real Volume Verification

The demo made **150 actual calls** to the existing Sprint A ranker through the instrumented path, persisted **599 impressions and 884 total events**, reconstructed one impression→click→apply→shortlist journey, and generated reports/plots from the saved stream. User actions are explicitly a **controlled interaction simulation**, not production traffic or hand-written rows.

## Offline vs Online Evaluation

Existing held-out NDCG@3 0.9012 and Recall@3 0.9167 establish offline context. They do not guarantee online lift; the controlled rates cannot substitute for randomized production validation. No ranker parameters were trained/tuned here.

## Failure / Fallback Behaviour

An intentional primary failure returned three valid fallback results with `fallback_ranker`, `fallback-v1`, `fallback_used=true` and sanitized reason. The event stream remained valid and reconstructable.

## Privacy

Only opaque platform identifiers are logged—no names, email addresses, phone numbers or raw profiles.

## Backend Handoff

Creation points, API mapping, required fields, retries/idempotency and degradation behavior are in `docs/HANDOFF_BACKEND_DATA_ANALYST.md`.

## Data Analyst Handoff

The handoff documents JSONL loading, join keys, funnel reconstruction, position analysis and model-version comparison.

## Project Structure

`src/` contains contracts/runtime logic; `data/` contains runtime JSONL; `docs/` contains contracts; `reports/` and `outputs/` contain measured evidence; `tests/` covers schema, lineage, completeness, metrics and fallback.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run Demo

```bash
python run_instrumentation_demo.py
```

## Run Tests

```bash
python -m pytest -q
```

## Generated Reports

Reports cover volume, joinability, position/model coverage, online-style metrics, one actual trace, failure injection and offline–online limits. Four plots visualize funnel, volume, position CTR and model-version exposure.

## Definition of Done

All schemas, IDs, positions, versions, joins, meaningful runtime volume, metric breakdowns, trace, fallback test and handoffs are implemented. Tests pass. The genuine remaining limitation is absence of production traffic/online causal validation.
