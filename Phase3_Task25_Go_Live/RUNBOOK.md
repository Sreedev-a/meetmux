# Production model-monitoring runbook

1. Acknowledge the page and identify affected window/model version.
2. Check availability, p95 latency, score variance, labeled quality, and input drift.
3. If integrity, quality, or degenerate-score alerts fire, remove the model from traffic and enable cached eligible-job rankings.
4. If latency/availability alone fails, scale healthy replicas; rollback if two windows remain outside SLO.
5. Preserve request IDs and aggregate metrics, avoiding raw personal data in alerts.
6. Close only after two healthy windows, a named owner, incident notes, and a follow-up issue.
