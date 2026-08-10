# Ranking Event Schema v1.0

All timestamps are timezone-aware UTC ISO 8601. IDs are opaque; no names, email addresses or phone numbers are logged.

## Common required envelope

`event_id`, `event_type`, `event_timestamp`, `request_id`, `ranking_id`, `impression_id`, `session_id`, `actor_id`, `item_id`, `item_type`, one-based `rank_position`, `model_name`, `model_version`, `feature_version`, and `schema_version` are required. Impression `score` is optional because fallback results may be unscored. Experiment/variant, application/shortlist IDs, context and metadata are conditional or optional. Model fields and original position are copied from the impression into outcomes (derived lineage fields).

```json
{"event_id":"evt_a","event_type":"impression","event_timestamp":"2026-08-10T11:22:26Z","request_id":"req_1","ranking_id":"rank_1","impression_id":"imp_1","session_id":"session_1","actor_id":"student_1","item_id":"j2","item_type":"job","rank_position":1,"score":0.97,"model_name":"recommendation_gate","model_version":"2.0.0","feature_version":"recommendation-features-v2","schema_version":"1.0","experiment_id":"ranking_growth_2026_08","variant":"control","fallback_used":false,"context":{"ranking_direction":"jobs_for_student"},"metadata":{}}
```

```json
{"event_id":"evt_b","event_type":"click","event_timestamp":"2026-08-10T11:22:27Z","request_id":"req_1","ranking_id":"rank_1","impression_id":"imp_1","session_id":"session_1","actor_id":"student_1","item_id":"j2","item_type":"job","rank_position":1,"model_name":"recommendation_gate","model_version":"2.0.0","feature_version":"recommendation-features-v2","schema_version":"1.0","fallback_used":false,"context":{},"metadata":{}}
```

```json
{"event_id":"evt_c","event_type":"apply","event_timestamp":"2026-08-10T11:22:28Z","request_id":"req_1","ranking_id":"rank_1","impression_id":"imp_1","session_id":"session_1","actor_id":"student_1","item_id":"j2","item_type":"job","rank_position":1,"model_name":"recommendation_gate","model_version":"2.0.0","feature_version":"recommendation-features-v2","schema_version":"1.0","application_id":"app_1","fallback_used":false,"context":{},"metadata":{}}
```

```json
{"event_id":"evt_d","event_type":"shortlist","event_timestamp":"2026-08-10T11:22:29Z","request_id":"req_1","ranking_id":"rank_1","impression_id":"imp_1","session_id":"session_1","actor_id":"student_1","item_id":"j2","item_type":"job","rank_position":1,"model_name":"recommendation_gate","model_version":"2.0.0","feature_version":"recommendation-features-v2","schema_version":"1.0","application_id":"app_1","shortlist_id":"short_1","fallback_used":false,"context":{},"metadata":{}}
```

Pydantic rejects unknown event types, blank IDs/versions, naive timestamps, non-positive positions, outcomes missing impression linkage, and apply/shortlist events missing required domain IDs.
