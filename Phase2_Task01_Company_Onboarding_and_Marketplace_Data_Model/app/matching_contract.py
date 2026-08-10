"""Reference feature-space demonstration; not a production ranking model."""

import argparse
import json
from pathlib import Path

from .feature_space import (
    align_feature_vectors,
    build_job_feature_vector,
    build_student_feature_vector,
    normalize_skill_name,
)
from .schemas import JobProfile, StudentProfile

ROOT = Path(__file__).resolve().parents[1]


def demonstrate(student_path: Path, job_path: Path) -> dict[str, object]:
    student = StudentProfile.model_validate_json(student_path.read_text(encoding="utf-8"))
    job = JobProfile.model_validate_json(job_path.read_text(encoding="utf-8"))
    student_vector = build_student_feature_vector(student)
    job_vector = build_job_feature_vector(job)
    aligned_student, aligned_job = align_feature_vectors(student_vector, job_vector)
    return {
        "label": "matching foundation / feature-space demonstration",
        "student_id": student.student_id,
        "job_id": job.job_id,
        "features": list(aligned_student),
        "student_vector": aligned_student,
        "job_threshold_vector": aligned_job,
        "required_features": sorted(normalize_skill_name(s) for s in job.required_skills),
        "preferred_features": sorted(normalize_skill_name(s) for s in job.preferred_skills),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student", type=Path, default=ROOT / "examples/sample_student.json")
    parser.add_argument("--job", type=Path, default=ROOT / "examples/sample_job.json")
    args = parser.parse_args()
    print(json.dumps(demonstrate(args.student, args.job), indent=2))


if __name__ == "__main__":
    main()
