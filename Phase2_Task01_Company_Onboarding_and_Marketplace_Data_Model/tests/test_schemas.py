import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.schemas import JobProfile, MatchRequest, MatchResponse, StudentProfile

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_student_score_validation(score: float) -> None:
    payload = load("sample_student.json")
    payload["verified_scores"]["python"] = score
    with pytest.raises(ValidationError):
        StudentProfile.model_validate(payload)


@pytest.mark.parametrize("threshold", [-1, 1.2])
def test_job_threshold_validation(threshold: float) -> None:
    payload = load("sample_job.json")
    payload["required_skills"]["python"] = threshold
    with pytest.raises(ValidationError):
        JobProfile.model_validate(payload)


def test_duplicate_or_overlapping_job_skills_rejected() -> None:
    payload = load("sample_job.json")
    payload["preferred_skills"]["PYTHON Programming"] = 0.4
    with pytest.raises(ValidationError):
        JobProfile.model_validate(payload)


def test_schemas_serialize_and_contract_samples_validate() -> None:
    student = StudentProfile.model_validate(load("sample_student.json"))
    job = JobProfile.model_validate(load("sample_job.json"))
    request = MatchRequest(student=student, job=job)
    response = MatchResponse.model_validate(load("sample_match_response.json"))
    assert MatchRequest.model_validate_json(request.model_dump_json()) == request
    assert MatchResponse.model_validate_json(response.model_dump_json()) == response
