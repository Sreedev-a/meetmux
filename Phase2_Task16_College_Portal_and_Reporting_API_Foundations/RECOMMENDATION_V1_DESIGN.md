# Recommendation v1 design

The v1 objective is to rank active jobs for a student using only verified competencies and explicit preferences. Candidate generation retrieves active jobs from verified companies and applies hard eligibility filters. Ranking uses the four versioned features/weights in `config/recommendation_v1.json`, with stable job ID tie-breaking. New users receive the transparent recent-eligible fallback.

`POST /v1/recommendations/jobs` accepts `student_id`, `limit`, and `request_id`; it returns `job_id`, score, eligibility, feature contributions, model/config version, and explanation. Offline gates are NDCG@5, Recall@5, coverage, and per-segment regression; online monitoring covers click/apply conversion, latency, empty results, warnings, and drift. Sensitive attributes are excluded. Rollout proceeds shadow, 10%, 50%, 100%, with rollback on any guardrail breach.
