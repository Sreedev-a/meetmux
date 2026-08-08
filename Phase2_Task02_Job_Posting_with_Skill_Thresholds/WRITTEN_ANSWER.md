# Job Posting with Skill Thresholds

I implemented a vector builder that canonicalizes common skill aliases, validates every competency threshold on a 0–100 scale, rejects collisions and required/optional overlap, and aligns each student/job pair to a deterministic sorted vocabulary. Student scores and job thresholds are normalized to `[0,1]`; a required-skill mask preserves hard eligibility semantics. Executing the solution generated vectors for four sample student/job pairs in both JSON and analysis-friendly CSV form, with missing skills correctly represented as zero.
