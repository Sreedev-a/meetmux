# Failure Handling & Resilience

I compared paired pre-paywall and post-paywall NDCG@3 values with a maximum tolerated regression of 0.02, both overall and within fresher, experienced, and remote segments. The executable gate emits a release/rollback decision and fails the process if any group breaches tolerance. On the supplied evaluation sample the mean relevance did not regress and every segment passed, so the release decision is `pass`.
