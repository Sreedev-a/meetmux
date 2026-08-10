# Backend and Data Analyst Handoff

## Backend

Call `InstrumentedRanker.rank` after ranking and immediately before serving visible results. It creates one `ranking_id`, one impression per result, and one-based positions without sorting. Return `ranking_id`/`impression_id` to clients. Click/apply/shortlist handlers must call `EventLogger` with the originating impression ID; apply/shortlist also require application IDs, and shortlist requires its ID. Validate before append. Use `event_id` as a unique ingestion key for retries. Preserve explicit fallback fields and monitor failures; never silently attribute fallback results to the primary version.

The local function contract corresponds to a future authenticated `POST /api/v1/events`; accept the v1 schema and respond `{ "accepted": true, "event_id": "..." }`. Authorization must verify the actor can emit the action while IDs remain opaque.

## Data Analyst

Read JSONL with `pandas.read_json(path, lines=True)`. Filter impressions, then join outcomes on `impression_id`; use `ranking_id` plus sorted `rank_position` to reconstruct a list. Compute CTR by grouping all events on `rank_position` and dividing click counts by impression counts. Group on `model_version` for impression, CTR, apply and shortlist rates, while controlling for experiment variant/position. Build the funnel with distinct event IDs and audit orphans before publication. `application_id` links application and shortlist business outcomes. UTC timestamps define ordering; `schema_version` controls compatibility.

The committed runtime log is controlled simulation evidence, not production behaviour. Production dashboards must label source/environment and require adequate exposure before model comparison.
