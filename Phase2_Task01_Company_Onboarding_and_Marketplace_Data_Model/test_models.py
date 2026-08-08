import json
import unittest
from pathlib import Path

from pydantic import ValidationError

from models import Job, MatchRequest

ROOT = Path(__file__).resolve().parent


class ContractTests(unittest.TestCase):
    def test_sample_contract(self):
        model = MatchRequest.model_validate_json((ROOT / "data/sample_match_request.json").read_text())
        self.assertEqual(len(model.jobs), 2)

    def test_threshold_bounds(self):
        payload = json.loads((ROOT / "data/sample_match_request.json").read_text())
        payload["jobs"][0]["required_skills"]["python"] = 101
        with self.assertRaises(ValidationError):
            MatchRequest.model_validate(payload)

    def test_skill_groups_cannot_overlap(self):
        with self.assertRaises(ValidationError):
            Job(job_id="job_1", company_id="co_1", required_skills={"sql": 60}, optional_skills={"sql": 40}, minimum_experience=0, locations=["Pune"], work_mode="remote", salary_lpa=5)


if __name__ == "__main__":
    unittest.main()
