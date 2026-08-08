# E-Sign Integration & Tamper-Evidence

I built parsing v0 for resumes and job descriptions. It maps exact, word-bounded aliases to canonical skills, retains every source evidence span, extracts stated years of experience, and emits document and parser versions for traceability. Execution parsed three real-shaped sample documents into structured JSON; tests cover aliases, experience extraction, and false substring matches. This deterministic baseline is intentionally conservative so later ontology enrichment remains auditable.
