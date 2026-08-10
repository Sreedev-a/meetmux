# Submission

**Task:** Phase 3 Sprint B Task 6

**Title:** Growth Instrumentation & North-Star Metrics

## Actual implementation and evidence

- Baseline: versioned ranking/fallback and offline evaluation existed; joinable ranked-event instrumentation did not.
- Schema: strict Pydantic `impression`, `click`, `apply`, `shortlist` events with v1.0 envelope.
- Runtime source: existing Sprint A recommendation service; actions: controlled interaction simulation, not production users.
- Requests/rankings: 150 / 150 unique.
- Events: 884 total—599 impressions, 169 clicks, 84 applies, 32 shortlists.
- Unique impression IDs: 599; unique event IDs: 884.
- Position coverage: 599/599 (100%); model-version coverage: 599/599 (100%).
- Outcome joinability: 285/285 (100%); schema validity: 884/884 (100%).
- North star: shortlist per ranked impression, 32/599 (5.34%) in controlled evidence.
- Guardrails: CTR/apply rates, offline quality, latency/availability, fallback/no-result, schema/orphan/duplicate coverage and fairness.
- Fallback: intentional model failure returned and logged three valid `fallback-v1` impressions; PASS.
- Offline context: prior held-out NDCG@3 0.9012 and Recall@3 0.9167; no causal online equivalence claimed.
- Tests: 19 passed.

## Files and commands

`src/` contains the runtime; `docs/` contains Backend/Analyst contracts; `data/generated_runtime_logs/` contains actual emitted JSONL; `reports/` and `outputs/` contain computed evidence; `tests/` covers schema, order, joins, duplicates, metrics and fallback.

```bash
python run_instrumentation_demo.py
python -m pytest -q
```

Submit the complete task folder. Recommended screenshots: console summary/tests, funnel/position charts, actual E2E trace, coverage reports and fallback report.
