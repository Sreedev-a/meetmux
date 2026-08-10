# Phase 3 Sprint B Task 7 — Activation & Onboarding Funnel Optimization

## Objective

Give zero-history candidates relevant, explained first-session jobs from onboarding signals, with controlled exploration, a never-empty fallback and Task 6-compatible measurement.

## Official Deliverables

Cold-start strategy, measured evidence where data permits, and a fallback that is non-empty whenever active inventory exists.

## Definition of Cold Start

Zero prior ranking interactions, clicks and applications; verified competencies and explicit onboarding preferences remain allowed.

## Existing Baseline and Available Data

The baseline is popularity/quality/recency over eligible jobs. Repository interaction and relevance files are fixtures; Task 6 events are controlled simulation. No genuine first-session cohort or online experiment exists, so behavioural lift is unavailable and documented in `BLOCKED.md`.

## Candidate Signals and Job Eligibility

The service normalizes existing PlaceMux-style skills and uses verified scores, role/location preferences and experience. Inactive, expired and clearly experience-ineligible jobs are hard-filtered before ranking.

## Cold-Start Strategy and Scoring

The explicit rule-based `cold-start-v1` weights skills 50%, role 18%, location 12%, experience 8%, quality 7% and freshness 5%. It uses no future behaviour.

## Exploration Strategy

At K=5, one eligible lower-ranked item (20%) is selected deterministically with seed 42. Results are unique and source-labelled.

## Never-Empty Fallback

Failure/insufficient results degrade to popular eligible jobs, then recent active jobs. Seven diverse runtime profiles, including forced failure, each returned five results: 100% non-empty. A truly empty active marketplace returns an honest empty response.

## Explainability

Each item exposes matched verified skills, gaps, role/location evidence, source, score and concise reason.

## First-Session Metrics

The intended primary metric is candidate-level first-session relevant-action (apply/shortlist) rate. Genuine values and lift are not available; no CTR/application statistics were fabricated.

## Baseline vs Cold-Start Evaluation

A controlled held-out engineering fixture with four candidates and eleven jobs produced NDCG@5 0.4317→0.8446 and Recall@5 0.7083→0.7917. The NDCG difference (+0.4129; +95.66%) is a fixture-only offline proxy, not activation lift.

## Offline vs Online Gap

Production causal validation requires randomized new-candidate assignment and genuine Task 6 outcomes. No weights were tuned against fixture labels.

## Task 6 Instrumentation Integration

The demo dynamically reuses Task 6's exact `RankingEvent`, JSONL store and logger. Five fresh-session impressions preserve ranking/impression IDs, positions, model version, source, exploration and fallback context.

## Cold-Start API

`POST /api/v1/recommendations/cold-start` accepts full, partial or minimal profiles; Pydantic validates IDs/scores/K and Flask returns 422 errors safely.

## Fresh Candidate E2E Demo

`fresh_candidate_001` has zero history, receives five explained recommendations, emits five Task 6 impressions, and then exercises forced fallback. No outcome is invented.

## Model Failure Behaviour

Forced failure returns five tier-1 popular/quality recommendations with `cold-start-fallback-v1`; PASS.

## Frontend Handoff

Request/response, loading/error/empty/fallback handling, ranking order and instrumentation responsibilities are documented in `docs/FRONTEND_HANDOFF.md`.

## Project Structure

`src/` service/API/evaluation; `docs/` strategy/contracts; `data/runtime_evidence/` emitted evidence; `reports/` measured findings; `outputs/` plots; `tests/` automated coverage.

## Setup, Demo and Tests

```bash
python -m pip install -r requirements.txt
python run_cold_start_demo.py
python -m pytest -q
```

## Generated Reports and Definition of Done

All strategy, baseline, exploration, fallback, API, explainability, failure, fixture evaluation, Task 6 integration and Frontend handoff artifacts are present. Live first-session lift remains explicitly blocked on production data/experiment availability.
