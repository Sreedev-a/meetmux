# Intentional Model-Unavailable Test

The final runtime request set `force_failure=True` on the existing Sprint A service. The service returned a valid deterministic fallback list; instrumentation logged **3 impressions** under ranking `rank_09e1dcee59724b52a6333022b308d05c`, with `model_name=fallback_ranker`, `model_version=fallback-v1`, `fallback_used=true`, and sanitized reason `injected_model_failure`. Normal event history remained valid and joinable. Result: **PASS**.
