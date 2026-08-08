# Reliability sign-off and growth hand-off

Decision is determined only by `outputs/reliability_signoff.json`. Approval requires p95 ≤100 ms, availability ≥99.5%, quality ≥0.80, fallback rate ≤1% at target load, verified forced-failure fallback, ≥50% measured headroom, and a working metrics endpoint.

Owner: ML Reliability Owner. Fallback: cached active-job rankings with `fallback=true`, no fabricated confidence, and an explicit reason. Rollback on quality/integrity breach, two consecutive latency/availability windows, or exhausted error budget.

Residual risks are owned, not hidden: production traffic and hardware can differ from local execution; the production observability deployment described in Phase 3 Task 25 still requires DevOps access. Growth work may use this signed local baseline only after staging repeats the load/failure test.
