# Profiling and optimization decision

The baseline profile showed query/job norm computation inside the per-job loop. The optimized path precomputes active-job norms once and computes the query norm once per request. Ranking semantics, stable tie-breaking, and floating-point scores remain identical.

The report uses measured wall-clock latency and CPU seconds per million requests as a hardware-local cost proxy; it does not invent cloud currency. Production capacity planning must rerun the same benchmark on deployment-class hardware. If model state is unavailable, the path returns precomputed active jobs with `fallback=true` and no model confidence.
