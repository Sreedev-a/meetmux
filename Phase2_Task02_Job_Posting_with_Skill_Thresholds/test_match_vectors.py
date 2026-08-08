import unittest
from match_vectors import normalize_skill, validate_thresholds, vectorize


class VectorTests(unittest.TestCase):
    def test_alias_mapping(self):
        self.assertEqual(normalize_skill("PostgreSQL"), "sql")

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            validate_thresholds({"python": 101})

    def test_alignment_and_missing_skill(self):
        row = vectorize({"student_id":"s", "verified_skills":{"python":80}}, {"job_id":"j", "required_skills":{"SQL":60,"Python":70}, "optional_skills":{}})
        self.assertEqual(row["vocabulary"], ["python", "sql"])
        self.assertEqual(row["student_vector"], [0.8, 0.0])


if __name__ == "__main__": unittest.main()
