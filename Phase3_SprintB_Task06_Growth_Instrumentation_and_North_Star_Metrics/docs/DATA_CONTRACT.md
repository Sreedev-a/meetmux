# Data Contract and Join Keys

```text
request_id → ranking_id → (item_id, impression_id, rank_position)
                              └─ impression_id → click/apply/shortlist
application_id ────────────────────────────────→ apply/shortlist
```

- `request_id` correlates the caller request; `ranking_id` uniquely identifies one ordered response.
- Each shown item receives one unique `impression_id`; `(ranking_id, rank_position)` reconstructs order.
- Outcomes must cite an existing `impression_id`. Repeated appearances of the same item therefore remain distinct.
- `application_id` joins apply to shortlist business objects; `shortlist_id` identifies the shortlist action.
- `event_id` is the idempotency/deduplication key. Duplicate IDs are rejected by the local store; production ingestion should enforce a unique constraint and treat a retry with identical content as already accepted.

JSONL is append-only, one validated JSON object per line. Consumers should parse UTC timestamps and filter/branch on `schema_version`. Additive optional fields are backward compatible within v1; removed fields or semantic changes require a new major schema version. `rank_position` is always one-based. Context identifiers are pseudonymous platform IDs, not raw PII.
