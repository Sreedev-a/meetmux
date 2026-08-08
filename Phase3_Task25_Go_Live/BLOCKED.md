# External production deployment blocker

The model-monitoring evaluator, SLO checks, dashboard/alert contract, runbook, normal-path evidence, and deliberately injected failure evidence are complete and reproducible locally.

The PDF's literal requirement “ML monitored in production” cannot be truthfully verified from this repository because no production telemetry endpoint, deployment target, observability account, or alert-routing credentials are available. No production event is claimed.

Minimum user/DevOps action: deploy `config/monitoring.json` to the production observability platform, connect sanitized inference metrics, route alerts to the real on-call destination, run a controlled failure injection during an approved window, and attach the resulting dashboard/alert evidence. Remove this blocker only after those external steps succeed.
