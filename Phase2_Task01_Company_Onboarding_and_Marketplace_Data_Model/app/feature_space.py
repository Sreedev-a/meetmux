"""Deterministic normalization and alignment for student/job skill features."""

import re
from collections.abc import Mapping

from .schemas import JobProfile, StudentProfile

SKILL_ALIASES = {
    "ml": "machine_learning",
    "machine_learning": "machine_learning",
    "python_programming": "python",
    "structured_query_language": "sql",
}


def normalize_skill_name(name: str) -> str:
    """Return a lowercase snake-case identifier, resolving known aliases."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("skill name must be a non-empty string")
    canonical = re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    if not canonical:
        raise ValueError("skill name must contain letters or numbers")
    return SKILL_ALIASES.get(canonical, canonical)


def _normalize_scores(scores: Mapping[str, float]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for raw_name, raw_score in scores.items():
        name = normalize_skill_name(raw_name)
        if name in normalized:
            raise ValueError(f"duplicate skill after normalization: {name}")
        score = float(raw_score)
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"score for {name} must be between 0 and 1")
        normalized[name] = score
    return dict(sorted(normalized.items()))


def build_student_feature_vector(student: StudentProfile) -> dict[str, float]:
    """Build a vector from verified scores only."""
    return _normalize_scores(student.verified_scores)


def build_job_feature_vector(job: JobProfile) -> dict[str, float]:
    """Build one threshold vector from required and preferred job skills."""
    return _normalize_scores({**job.required_skills, **job.preferred_skills})


def align_feature_vectors(
    student_vector: Mapping[str, float], job_vector: Mapping[str, float]
) -> tuple[dict[str, float], dict[str, float]]:
    """Align vectors over their union; absent features deterministically become 0."""
    student = _normalize_scores(student_vector)
    job = _normalize_scores(job_vector)
    features = sorted(set(student) | set(job))
    return (
        {feature: student.get(feature, 0.0) for feature in features},
        {feature: job.get(feature, 0.0) for feature in features},
    )


def validate_feature_space(student: StudentProfile, job: JobProfile) -> bool:
    student_vector = build_student_feature_vector(student)
    job_vector = build_job_feature_vector(job)
    aligned_student, aligned_job = align_feature_vectors(student_vector, job_vector)
    return list(aligned_student) == list(aligned_job)
