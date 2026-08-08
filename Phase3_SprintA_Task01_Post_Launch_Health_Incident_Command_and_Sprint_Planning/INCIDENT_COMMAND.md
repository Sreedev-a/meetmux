# Incident command and hand-off

Incident commander: ML Reliability Owner. Operations lead: Backend on-call. Data/diagnostics: Data Platform. Communications: Product Operations.

SEV-1 is widespread unavailability, corrupt/unsafe output, or quality below the hard floor; immediately enable cached eligible rankings and rollback. SEV-2 is sustained SLO degradation or a segment-specific quality regression; stop rollout and assign an owner. Preserve request IDs, model/config version, aggregate signals, and a UTC timeline without copying personal data into tickets.

The generated `ranked_defects.csv` and `phase3_backlog.csv` are the Backend/Data hand-off. Each defect has quantified impact, an owner, priority, and acceptance criterion.
