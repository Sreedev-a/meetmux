# Student ↔ Job Feature Space

## Why a shared space is necessary

Student evidence and job requirements must use identical feature identifiers and the same numeric scale. Otherwise labels such as `ML` and `machine-learning` become unrelated dimensions and thresholds cannot be evaluated reliably.

## Representations

`StudentProfile.verified_scores` maps arbitrary skill identifiers to verified assessment scores. Self-reported skills are metadata and do not enter the v1 verified vector. Education, experience, availability and preferences are typed context for later filters and ranking features.

`JobProfile.required_skills` maps skills to minimum thresholds. Every required threshold contributes to eligibility. `preferred_skills` uses the same representation but is optional: it may improve future ranking, but a miss does not make a candidate ineligible.

## Scale and normalization

Scores and thresholds use `0.0` (no demonstrated competency) through `1.0` (maximum demonstrated competency). Values outside this inclusive range are rejected.

Labels are trimmed, lowercased, converted to snake case and passed through an explicit alias map. `Python Programming`, `python`, and `PYTHON` become `python`; `Machine Learning`, `machine-learning`, and `ML` become `machine_learning`. Unknown skills remain extensible normalized identifiers. Empty labels and duplicate canonical skills are rejected rather than overwritten.

## Alignment and missing skills

Alignment uses the sorted union of features. Missing features have value `0.0`; required job skills are never dropped. Student-only skills receive job threshold `0.0`. The aligned dictionaries therefore have identical ordered keys.

## Worked example

| Feature | Student | Job threshold | Group |
|---|---:|---:|---|
| `data_analysis` | 0.72 | 0.50 | preferred |
| `machine_learning` | 0.82 | 0.65 | required |
| `python` | 0.90 | 0.75 | required |
| `sql` | 0.76 | 0.60 | required |

If the job also requires `cloud_computing: 0.55`, alignment retains it and assigns the student `0.0`, exposing the gap.

## Validation and extensibility

Schemas reject malformed scores, empty identifiers, unknown fields, negative experience, overlapping groups and normalized duplicates. A future ontology can expand aliases behind the same versioned contract. Later versions can add experience, location, recency, confidence, embeddings or learned weights without changing v1 semantics.
