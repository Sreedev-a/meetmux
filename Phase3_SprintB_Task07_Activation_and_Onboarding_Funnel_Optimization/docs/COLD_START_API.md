# Cold-Start API

`POST /api/v1/recommendations/cold-start` accepts `{candidate, k=5, exploration_fraction=0.2, force_model_failure=false}`. `candidate_id` is required; scores must be 0–1. Skills, role/location preferences, employment types and experience are optional. `k` is 1–20 and exploration is 0–0.5.

The 200 response includes candidate/user state, ranking/model IDs, fallback state/tier/reason and positioned recommendations containing score, source, exploration flag, evidence-derived reason, matches and gaps. Invalid requests return 422 `{error:"validation_error", details:[...]}`. Empty marketplace is a valid 200 with `reason=no_active_jobs`.
