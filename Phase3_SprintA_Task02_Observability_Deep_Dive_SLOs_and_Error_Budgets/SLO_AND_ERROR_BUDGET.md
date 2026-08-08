# Intelligence-layer SLO and error budget

Owner: ML Reliability Owner. Over rolling five-minute windows, p95 model latency must be ≤100 ms and availability ≥99.5%. Labeled quality must remain ≥0.80 over a rolling labeled cohort, and prediction-score standard deviation must stay ≥0.03 to detect constant/degenerate output.

At 99.5% availability, a 30-day month permits 216 unavailable minutes. Burn ≥50% triggers investigation and blocks nonessential model changes; burn ≥100% freezes risky releases and invokes fallback/rollback. Quality or integrity failures can halt rollout even when availability budget remains. Alerts route to ML Reliability on-call and are handed to DevOps through `config/alert_rules.yml`.

Fallback returns cached eligible-job rankings with `fallback=true`, a model-version marker, and no fabricated confidence. Recovery requires two healthy windows and incident ownership.
