import unittest
from fairness_signoff import evaluate, generate_fixture


class FairnessSignoffTests(unittest.TestCase):
    def test_reproducible_fixture(self):
        self.assertEqual(generate_fixture(10), generate_fixture(10))

    def test_signoff_passes_documented_fixture(self):
        result = evaluate(generate_fixture())
        self.assertTrue(result["approved"])
        self.assertGreaterEqual(result["summary"]["disparate_impact_ratio"], .8)

    def test_fail_closed_on_small_sample(self):
        self.assertFalse(evaluate(generate_fixture(20))["approved"])


if __name__ == "__main__":
    unittest.main()
