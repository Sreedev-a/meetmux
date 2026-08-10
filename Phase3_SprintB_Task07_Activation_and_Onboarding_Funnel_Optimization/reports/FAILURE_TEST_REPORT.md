# Failure Test

Forced `RuntimeError("forced_model_failure")` activated tier-1 fallback. The response remained valid and non-empty with five positioned, explained results; `fallback_used=true`, `model_version=cold-start-fallback-v1`, and the original ranking response was not corrupted. Result: **PASS**.
