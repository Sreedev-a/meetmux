# Genuine First-Session Lift Blocker

The repository contains no production first-session candidate cohort with pre-interaction onboarding snapshots, randomized treatment assignment, and genuine click/apply/shortlist outcomes. Task 6 events are explicitly controlled simulation; Sprint A interaction logs and Phase 2 relevance data are fixtures. Therefore genuine online first-session relevant-action lift cannot be measured honestly.

Completed instead: a controlled held-out engineering fixture evaluation, runtime API/demo, Task 6-compatible impressions, exploration, fallbacks, and metric plumbing. Next, run a production experiment that randomizes eligible new candidates between popularity baseline and `cold-start-v1`, logs assignment/impressions/outcomes through Task 6, uses onboarding-only features, and compares candidate-level first-session apply/relevant-action rates with position, reliability and fairness guardrails.
