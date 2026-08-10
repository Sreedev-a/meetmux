# Frontend Handoff

After onboarding, POST the candidate’s verified scores and available preferences to `/api/v1/recommendations/cold-start`; show loading state until 200. Render results in supplied position order, display `reason`, and retain `ranking_id` plus each result’s Task 6 impression ID in the integrated response path for click/apply attribution. Bad input (422) should map field details to onboarding UI.

Show a subtle discovery label for `exploration=true` if product design approves. Do not hide `fallback_used`; normal content remains displayable. If `reason=no_active_jobs`, show an honest marketplace-empty state and retry later. Never reorder client-side because rank position is analytics-critical. Model fields are diagnostic, not user-facing labels.
