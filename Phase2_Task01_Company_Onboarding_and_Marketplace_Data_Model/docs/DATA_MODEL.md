# Marketplace Matching Data Model

```text
Company
└── Job
    ├── Required skill thresholds
    └── Preferred skill thresholds

Student
└── Verified competency scores

Student + Job
└── Common feature space → Matching service → Match result
```

`Company` owns jobs but company attributes are not competency signals. Each job describes required and preferred threshold maps. Each student separates verified scores—the v1 matching input—from self-reported and contextual data. Platform-owned IDs remain opaque, so the service does not assume a database implementation.

Normalization creates a common key space and alignment preserves the union of features. The same representation supports student-to-job and job-to-student retrieval. Per-skill evidence enables auditable eligibility decisions, gaps and marketplace explanations.

The model can later support search filters, shortlisting, ranking, recommendations and feature stores. New metadata or algorithms belong behind a versioned contract. Sensitive traits are intentionally absent; production governance should also track assessment provenance, verification time, consent, confidence and retention.
