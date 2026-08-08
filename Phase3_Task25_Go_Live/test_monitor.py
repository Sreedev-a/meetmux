import unittest
from monitor import generate_logs, summarize


class MonitorTests(unittest.TestCase):
    def test_normal_window_healthy(self):
        rows = [r for r in generate_logs() if r["window"] == "normal"]
        self.assertTrue(summarize(rows)["healthy"])

    def test_injected_failure_pages(self):
        rows = [r for r in generate_logs() if r["window"] == "injected_failure"]
        self.assertIn("PAGE_DEGENERATE_SCORES", summarize(rows)["alerts"])
        self.assertIn("PAGE_LATENCY", summarize(rows)["alerts"])


if __name__ == "__main__":
    unittest.main()
