# Phase 2 Task 1 — Company Onboarding & Marketplace Data Model

## Objective

Define the stable matching foundation that transforms verified student competencies and job thresholds into aligned, validated feature vectors. This is a data-model and API-contract deliverable, not a trained production ranking model.

## Official requirements

- Define and document the student ↔ job feature space.
- Specify a versioned matching API contract with Backend.

## Architecture

```text
Student verified scores ─┐
                         ├─ normalize → align → matching service contract → result
Job skill thresholds ────┘
```

Pydantic schemas provide strict transport validation. Pure functions canonicalize arbitrary skill labels and align dictionary vectors. A lightweight module demonstrates the transformation using fictional JSON fixtures.

## Feature spaces

Students use verified competency scores on the inclusive `0.0–1.0` scale; self-reported skills are deliberately excluded from the verified v1 vector. Jobs express required and preferred thresholds on that same scale. Required misses affect eligibility; preferred misses are ranking signals only.

Normalization converts labels to canonical snake case and resolves a small transparent alias table. Alignment uses the union of keys. Any missing student skill becomes `0.0`, ensuring required skills are never silently discarded. See [docs/FEATURE_SPACE.md](docs/FEATURE_SPACE.md).

## API contract

The primary route is `POST /api/v1/match/student-job`. Future-compatible batch contracts rank jobs for a student and students for a job. Shapes, validation, errors and versioning are detailed in [docs/MATCHING_API_CONTRACT.md](docs/MATCHING_API_CONTRACT.md).

## Project structure

```text
app/       schemas, normalization/alignment, demonstration
docs/      feature-space, API-contract and data-model decisions
examples/  student, job and illustrative response JSON
tests/     schema and feature-space tests
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Keep `.venv` uncommitted. From this task directory, run:

```bash
python -m app.matching_contract
python -m pytest -q
```

## Example output

The demo prints one JSON object labeled `matching foundation / feature-space demonstration`, with aligned `student_vector` and `job_threshold_vector`. Its features include `data_analysis`, `docker`, `machine_learning`, `python`, and `sql`; Docker is `0.0` for the student because no verified Docker score exists.

## Deliverables

- Strict student, job, request, response, explanation and error schemas
- Extensible skill normalization and deterministic vector alignment
- Backend contracts for single and bidirectional ranking requests
- Data-model and feature-space documentation with sample payloads
- Executable demonstration and automated validation tests
