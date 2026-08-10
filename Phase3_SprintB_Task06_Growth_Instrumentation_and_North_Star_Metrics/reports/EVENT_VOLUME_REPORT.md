# Event Volume Report

This evidence is actual runtime output from **controlled interaction simulation**, not production traffic or hand-written rows. The existing ranker was called 150 times through the instrumented flow.

| Measure | Actual |
|---|---:|
| Ranking requests / unique ranking IDs | 150 / 150 |
| Impressions / unique impression IDs | 599 / 599 |
| Clicks | 169 |
| Applies | 84 |
| Shortlists | 32 |
| Total events | 884 |
| Schema-valid persisted events | 100.00% |

UTC range: `2026-08-10T11:24:33.213641+00:00` to `2026-08-10T11:24:34.336767+00:00`. Model versions: 2.0.0, fallback-v1. Event IDs are unique: 884 / 884.
