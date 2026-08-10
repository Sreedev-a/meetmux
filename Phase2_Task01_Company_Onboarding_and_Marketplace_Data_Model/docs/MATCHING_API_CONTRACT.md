# Backend Matching API Contract

## Common conventions

- Base path `/api/v1`, JSON/UTF-8. Scores and thresholds use inclusive `0.0–1.0`.
- Unknown fields are rejected; authentication is handled by the platform gateway.
- `matching_version` selects behavior and responses expose `model_version`. Algorithm changes preserving semantics do not break the contract; breaking JSON or semantic changes use `/api/v2`.

## `POST /api/v1/match/student-job`

Validates, aligns and matches one student and job. `student` and `job` are required; `matching_version` is optional and defaults to `feature-space-v1`. Student requires `student_id`, `name`, and non-empty `verified_scores`. Job requires `job_id`, `company_id`, `title`, and `required_skills`.

```json
{"student":{"student_id":"STU001","name":"Candidate One","verified_scores":{"python":0.90,"machine_learning":0.82,"sql":0.76}},"job":{"job_id":"JOB001","company_id":"COMP001","title":"Junior ML Engineer","required_skills":{"python":0.75,"machine_learning":0.65,"sql":0.60}},"matching_version":"feature-space-v1"}
```

A `200` returns `student_id`, `job_id`, normalized `match_score`, `eligible`, `matched_skills`, `skill_gaps`, `feature_breakdown`, and `model_version`. The sample response is illustrative, not a promised production algorithm result. Eligibility requires every required threshold; preferred gaps do not fail eligibility.

## `POST /api/v1/match/jobs-for-student`

Ranks jobs for one student. Request: `{ "student": StudentProfile, "jobs": [JobProfile], "limit": 10, "matching_version": "feature-space-v1" }`. Student and a non-empty jobs array are required; limit is optional (`1–100`). Response: `{ "student_id": "STU001", "results": [MatchResponse], "total_evaluated": 12, "model_version": "matching-foundation-v1" }`. Sort descending by score, then `job_id`.

## `POST /api/v1/match/students-for-job`

Ranks students for one job. Request: `{ "job": JobProfile, "students": [StudentProfile], "limit": 10, "matching_version": "feature-space-v1" }`. Job and a non-empty students array are required; limit is optional (`1–100`). Response: `{ "job_id": "JOB001", "results": [MatchResponse], "total_evaluated": 25, "model_version": "matching-foundation-v1" }`. Sort descending by score, then `student_id`.

The ranking routes define future-compatible shapes; v1 must not imply a trained ranking model.

## Errors and validation

- `400`: invalid JSON or unsupported version.
- `422`: schema errors, empty IDs, invalid ranges, normalized duplicates, or required/preferred overlap.
- `500`: unexpected service failure (`503` may represent temporary unavailability).

```json
{"error":{"code":"VALIDATION_ERROR","message":"Request validation failed","details":[{"path":"student.verified_scores.python","reason":"must be between 0 and 1"}]}}
```

Backend should pass correlation IDs via headers, avoid logging profile payloads, and treat IDs as opaque.
