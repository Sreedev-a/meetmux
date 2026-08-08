# Scaling and DevOps hand-off

Target: sustain the measured Task 4 target QPS at ≤100 ms p95 and ≤1% fallback, with at least 50% concurrency headroom. The local capacity is eight inference slots; the report identifies the first measured degraded concurrency and fallback rate.

- Autoscale on in-flight requests, queue depth, p95, and CPU: minimum 2 replicas; target 60% slot utilization; scale out after two 30-second windows; scale in only after 10 quiet minutes.
- Keep 50% spare capacity and distribute across failure domains. Use readiness probes so unloaded/corrupt replicas never receive traffic.
- Precompute active-job vectors and cache popular eligible rankings. Micro-batch offline refreshes; keep online personalized scoring request-based.
- Bound queues and deadlines. On overload or model failure, immediately return cached eligible rankings with `fallback=true`; never retry-storm the model.
- Re-run `load_test.py` on deployment-class hosts and during an approved staging soak before setting production replica counts.

Owner: DevOps Platform with ML Reliability. Required dashboard: QPS, concurrency, queue depth, p50/p95/p99, fallback/error rate, quality, replica count, saturation, and model version.
