# Receipts, Refunds & Reconciliation

I implemented a spend-quality guardrail that warns below a documented 0.70 fit threshold and escalates below 0.45. Each warning includes the score, policy thresholds, skill-gap reasons, severity, and acknowledgment requirement. It remains advisory to preserve user agency while ensuring candidates see the risk before paying. Actual execution produced one normal, one medium-risk, and one high-risk decision, with boundary behavior covered by tests.
