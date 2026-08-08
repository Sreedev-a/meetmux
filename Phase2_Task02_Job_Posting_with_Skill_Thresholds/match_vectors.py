"""Generate aligned competency vectors and validate job thresholds."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def normalize_skill(name: str) -> str:
    aliases = {"py": "python", "python3": "python", "postgres": "sql", "postgresql": "sql", "ml": "machine_learning"}
    key = "_".join(name.strip().lower().replace("-", " ").split())
    return aliases.get(key, key)


def validate_thresholds(skills: dict[str, float]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for raw_name, raw_score in skills.items():
        name, score = normalize_skill(raw_name), float(raw_score)
        if not 0 <= score <= 100:
            raise ValueError(f"threshold for {name} must be between 0 and 100")
        if name in normalized:
            raise ValueError(f"duplicate normalized skill: {name}")
        normalized[name] = score
    if not normalized:
        raise ValueError("at least one skill threshold is required")
    return normalized


def vectorize(student: dict, job: dict) -> dict:
    required = validate_thresholds(job["required_skills"])
    optional = validate_thresholds(job["optional_skills"]) if job.get("optional_skills") else {}
    if set(required) & set(optional):
        raise ValueError("required and optional skills overlap")
    scores = {normalize_skill(k): float(v) for k, v in student["verified_skills"].items()}
    vocabulary = sorted(set(required) | set(optional))
    return {
        "student_id": student["student_id"],
        "job_id": job["job_id"],
        "vocabulary": vocabulary,
        "student_vector": [scores.get(skill, 0.0) / 100 for skill in vocabulary],
        "threshold_vector": [(required | optional)[skill] / 100 for skill in vocabulary],
        "required_mask": [1 if skill in required else 0 for skill in vocabulary],
    }


def main() -> None:
    data = json.loads((ROOT / "data/sample_marketplace.json").read_text())
    rows = [vectorize(student, job) for student in data["students"] for job in data["jobs"]]
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    (out / "match_vectors.json").write_text(json.dumps(rows, indent=2) + "\n")
    with (out / "match_vectors.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["student_id", "job_id", "skill", "student_score", "threshold", "required"])
        writer.writeheader()
        for row in rows:
            for i, skill in enumerate(row["vocabulary"]):
                writer.writerow({"student_id":row["student_id"], "job_id":row["job_id"], "skill":skill, "student_score":row["student_vector"][i], "threshold":row["threshold_vector"][i], "required":row["required_mask"][i]})
    print(json.dumps({"pairs": len(rows), "rows": sum(len(r["vocabulary"]) for r in rows), "status": "validated"}, indent=2))


if __name__ == "__main__":
    main()
