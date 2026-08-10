# Cold-Start Strategy

A cold-start candidate has zero prior rankings, clicks and applications but may have onboarding data. `cold-start-v1` uses normalized verified competencies (50%), role preference (18%), location/remote fit (12%), experience suitability (8%), job quality (7%) and freshness (5%). It first filters inactive, expired and clearly experience-ineligible jobs. Scores, matched skills and gaps drive explanations. No behavioural/future outcome field enters scoring.

The system returns exploitation plus controlled eligible exploration, then hierarchical fallback. It is deterministic/rule-based—not a trained neural model—and the weights remain explicit configuration for later validation.
