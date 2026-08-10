# Baseline and Success Bar

> You can reconstruct exactly what was shown, in what order, by which model, and what happened next.

## Inspected baseline

The repository already had job-ranking logic (`Phase2_Task17...`), an integrated versioned ranking service with explicit fallback (`Phase3_SprintA_Task05...`), application/shortlist-shaped artifacts, and held-out offline recommendation validation (`Phase2_Task20...`: NDCG@3 0.9012, Recall@3 0.9167). It did **not** have a persisted ranked-impression schema or joinable click/apply/shortlist lineage. Existing interaction CSVs are fixtures and were not treated as production traffic.

## Measurable bar

| Control | Target | Executed result |
|---|---:|---:|
| Served-result impression coverage | 100% | 599/599 (100%) |
| Valid one-based position | 100% | 599/599 (100%) |
| Impression model version | 100% | 599/599 (100%) |
| Outcome-to-impression joinability | 100% | 285/285 (100%) |
| Persisted schema validity | 100% | 884/884 (100%) |
| Unique event identifiers | 100% | 884/884 (100%) |

The run uses controlled interaction simulation through the real implemented path, not production users. Online lift remains unmeasured.
