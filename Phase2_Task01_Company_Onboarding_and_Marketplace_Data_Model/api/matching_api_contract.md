# Matching API Contract v1

`POST /v1/matches/jobs` accepts one `MatchRequest` and returns `MatchResponse`. Authentication is handled by the platform gateway; `request_id` is the idempotency/correlation key. A `200` response contains ranked results, `422` identifies schema violations, and `503` signals a retryable matching-service failure.

The canonical machine-readable request contract is `match_request.schema.json`. The response includes the feature-space version, normalized score, eligibility, and per-feature contributions. Backends must preserve skill names in lowercase ontology form and treat missing verified skills as zero, never as an inferred score.
