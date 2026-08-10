# Submission

**Task:** Phase 2 Task 1

**Title:** Company Onboarding & Marketplace Data Model

## What was implemented

A Pydantic-based student/job data model, normalized shared skill feature space, deterministic missing-skill policy, versioned Backend matching contract, sample payloads, demonstration and automated tests.

## Files created

- `app/`: schemas, feature construction/alignment, runnable contract demonstration
- `docs/`: feature-space, matching API and marketplace data-model documentation
- `examples/`: fictional student/job fixtures and illustrative match response
- `tests/`: schema validation, serialization, normalization and alignment tests
- `README.md`, `WRITTEN_ANSWER.md`, `requirements.txt`

## Run and verify

From this folder after installing `requirements.txt`:

```bash
python -m app.matching_contract
python -m pytest -q
```

The demo should print aligned student and job dictionaries with identical keys and a zero student value for missing verified Docker competency. Tests should report all cases passed.

## Submission scope

Submit the entire `Phase2_Task01_Company_Onboarding_and_Marketplace_Data_Model/` folder. Useful screenshots show the demo JSON, passing pytest summary, and the GitHub folder containing the three documents.
