# Submission

**Task:** Phase 3 Sprint B Task 7

**Title:** Activation & Onboarding Funnel Optimization

- Baseline: popularity + quality + recency over eligible jobs.
- Strategy: onboarding-only weighted content/competency ranker (`cold-start-v1`).
- Data: controlled runtime/held-out engineering fixture; no genuine first-session history.
- Evaluation: four held-out fixture candidates, eleven jobs, K=5; no weight tuning.
- Exploration: deterministic eligible 20% (one of five normal results).
- Offline proxy: NDCG@5 0.4317→0.8446 (+0.4129, +95.66%); Recall@5 0.7083→0.7917.
- Behavioural action/lift metrics: unavailable; not fabricated.
- Runtime coverage: seven profiles, 100% non-empty; forced-fallback rate 14.29%.
- Failure test: PASS, five `cold-start-fallback-v1` recommendations.
- Task 6: exact schema/logger reused for five fresh-candidate impressions.
- API: `POST /api/v1/recommendations/cold-start`.
- Tests: run `python -m pytest -q`; demo: `python run_cold_start_demo.py`.

Submit the complete task folder. Suggested screenshots: passing tests/demo summary, baseline comparison, fallback coverage, fresh trace, API contract and `BLOCKED.md` production experiment requirement.
