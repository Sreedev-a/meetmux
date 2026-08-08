import json
from pathlib import Path

from models import MatchRequest

ROOT = Path(__file__).resolve().parent


def main() -> None:
    payload = json.loads((ROOT / "data" / "sample_match_request.json").read_text())
    request = MatchRequest.model_validate(payload)
    schema = MatchRequest.model_json_schema()
    (ROOT / "api" / "match_request.schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    report = {
        "valid": True,
        "request_id": request.request_id,
        "student_count": 1,
        "job_count": len(request.jobs),
        "feature_space_version": "1.0.0",
        "validated_features": ["verified_skill_fit", "experience_fit", "location_fit", "work_mode_fit", "salary_fit"],
    }
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "contract_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
