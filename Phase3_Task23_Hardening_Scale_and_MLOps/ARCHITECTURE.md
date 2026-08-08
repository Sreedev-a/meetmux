# MLOps foundation

The local registry uses immutable semantic versions, artifact SHA-256 checksums, lineage, metrics, features, approval, and an explicit lifecycle stage. Production consumers resolve a pinned version; promotion changes registry metadata through a reviewed pipeline, never by overwriting an artifact.

The offline feature store keys rows by entity and event time, with creation time retained for leakage analysis. Training retrieval selects the latest event at or before the observation timestamp. An online implementation would publish the same feature-view contract to a low-latency key-value store and monitor freshness, null rates, skew, latency, drift, and serving errors.
