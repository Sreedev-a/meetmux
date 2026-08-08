# Company Onboarding & Marketplace Data Model

I defined matching feature space v1.0.0 across verified competency fit, experience, location, work mode, and salary. Skill fit is dominant and required thresholds determine eligibility; the remaining features rank eligible and near-eligible opportunities. Sensitive attributes are excluded.

The backend contract is represented by validated Pydantic models and an exported JSON Schema. It accepts a correlated student-plus-jobs request and returns bounded scores, eligibility, feature contributions, and the feature-space version. The executable sample confirms two marketplace jobs validate correctly, while tests reject out-of-range thresholds and overlapping required/optional skill definitions.
