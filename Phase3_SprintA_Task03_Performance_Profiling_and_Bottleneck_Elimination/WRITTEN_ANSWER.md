# Performance Profiling & Bottleneck Elimination

I profiled the complete matching loop before optimizing and identified repeated normalization as the main avoidable work. The optimized path precomputes active-job norms and computes the query norm once. Repeated benchmarks record mean, median, p95, maximum latency, speedup, p95 reduction, and CPU-seconds-per-million cost proxy. Top-10 IDs and scores must match exactly, preventing a hidden quality trade-off, and p95 must meet the 100 ms SLO. A forced unavailable-model call verifies the explicit fallback.
