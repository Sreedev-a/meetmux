# North-Star and Guardrail Metrics

## Primary design choice

**Qualified shortlist rate per ranked impression = unique shortlisted originating impressions / ranked impressions.** This is an implementation choice because the brief does not prescribe a north star. It is closer to marketplace hiring value than click volume and remains attributable to exposure. The controlled run computed 32/599 = **5.34%**; this validates computability, not a production target or lift claim.

## Funnel and breakdowns

- CTR = clicks / impressions: 28.21%
- Apply rate per impression = applies / impressions: 14.02%
- Apply rate per click = applies / clicks: 49.70%
- Shortlist rate per application = shortlists / applications: 38.10%
- Shortlist rate per impression = shortlists / impressions: 5.34%

Position-aware CTR/apply/shortlist rates must accompany aggregate metrics because position drives exposure. Model-version breakdowns enable online comparison but require randomized or controlled experiment assignment before causal conclusions.

Guardrails: latency/availability, fallback rate, no-result rate, position/model logging coverage, schema validity, orphan rate, duplicate rate, application quality, fairness and offline ranking quality. Do not optimize clicks alone.
