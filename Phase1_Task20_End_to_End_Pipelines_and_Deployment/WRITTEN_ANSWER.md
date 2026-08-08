# End-to-End Pipelines & Deployment

I deployed the versioned Iris preprocessing-and-classification pipeline behind a Flask API. At startup, the loader reads the artifact manifest and metadata, verifies the model's SHA-256 checksum, and loads the complete fitted pipeline. `GET /health` reports service/model readiness, while `POST /predict` accepts four bounded numeric measurements and returns the class, species, confidence, and model version.

The service handles malformed JSON, wrong content types, schema violations, and internal prediction failures with explicit HTTP status codes and structured JSON. Automated endpoint tests cover the health check, successful real-shaped inference, missing/invalid fields, and non-JSON input. The committed latency report is produced from 200 warm local requests and evaluates the measured p95 against a documented 100 ms local acceptance threshold.
