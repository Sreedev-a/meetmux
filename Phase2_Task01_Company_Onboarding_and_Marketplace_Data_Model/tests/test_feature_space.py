import pytest

from app.feature_space import (
    align_feature_vectors,
    build_job_feature_vector,
    build_student_feature_vector,
    normalize_skill_name,
)
from app.schemas import JobProfile, StudentProfile


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("Python Programming", "python"), ("PYTHON", "python"), ("machine-learning", "machine_learning"), ("ML", "machine_learning")],
)
def test_skill_normalization(raw: str, expected: str) -> None:
    assert normalize_skill_name(raw) == expected


def test_missing_student_skill_becomes_zero_and_features_align() -> None:
    student = StudentProfile(student_id="STU001", name="Candidate", verified_scores={"Python": 0.9})
    job = JobProfile(job_id="JOB001", company_id="COMP001", title="ML Engineer", required_skills={"python": 0.75, "SQL": 0.6}, preferred_skills={"ML": 0.5})
    aligned_student, aligned_job = align_feature_vectors(
        build_student_feature_vector(student), build_job_feature_vector(job)
    )
    assert list(aligned_student) == list(aligned_job)
    assert aligned_student == {"machine_learning": 0.0, "python": 0.9, "sql": 0.0}
    assert aligned_job == {"machine_learning": 0.5, "python": 0.75, "sql": 0.6}


def test_duplicate_aliases_in_student_vector_rejected() -> None:
    student = StudentProfile(student_id="STU001", name="Candidate", verified_scores={"ML": 0.8, "machine learning": 0.9})
    with pytest.raises(ValueError, match="duplicate skill"):
        build_student_feature_vector(student)
