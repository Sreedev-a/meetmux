# Failure and Fallback Contract

If the primary ranker raises or reports unavailability, the existing Sprint A service supplies a deterministic safe list. Instrumentation does not hide the degradation: it records `model_name=fallback_ranker`, `model_version=fallback-v1`, `fallback_used=true`, and a sanitized `fallback_reason` on every resulting impression. Positions and unique lineage IDs are still assigned normally.

The executed intentional failure produced three valid fallback impressions without corrupting the preceding stream. A production API should expose degraded status in response metadata, alert on fallback rate, avoid returning raw exception/PII, and fail safely with an explicit empty result only if fallback itself fails.
