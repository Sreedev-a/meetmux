# Never-Empty Fallback

Primary personalized ranking falls back to: (1) popular/high-quality eligible jobs; then (2) recent active jobs if strict candidate eligibility yields none. With any active inventory this returns at least one item. A genuinely empty active marketplace returns `recommendations=[]` and `reason=no_active_jobs`; jobs are never invented.

Forced failure records `fallback_used=true`, tier 1, `cold_start_fallback` and `cold-start-fallback-v1`. The executed case returned five recommendations.
