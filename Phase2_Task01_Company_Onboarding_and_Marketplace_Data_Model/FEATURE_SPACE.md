# Student ↔ Job Feature Space v1.0.0

| Feature | Student source | Job source | Normalization | Initial weight |
|---|---|---|---|---:|
| Verified skill fit | verified competency scores | required/optional thresholds | weighted threshold attainment `[0,1]` | 0.55 |
| Experience fit | years of experience | minimum experience | `min(years/minimum, 1)` | 0.15 |
| Location fit | preferred locations | offered locations | exact normalized overlap | 0.10 |
| Work-mode fit | accepted modes | job mode | membership flag | 0.10 |
| Salary fit | expectation | offered salary | `min(offered/expected, 1)` | 0.10 |

Eligibility requires every required skill to meet its stated threshold. Ranking score is a weighted sum and is separate from eligibility so near-matches remain explainable. Sensitive attributes and proxies are excluded. Inputs carry source verification status upstream; only verified competency scores enter v1.
