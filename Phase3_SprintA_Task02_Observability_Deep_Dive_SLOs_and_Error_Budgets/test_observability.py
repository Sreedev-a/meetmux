import unittest
from observability import evaluate,fixture
class Tests(unittest.TestCase):
 def rows(self,w): return [r for r in fixture() if r["window"]==w]
 def test_healthy(self): self.assertEqual(evaluate(self.rows("healthy"))["alerts"],[])
 def test_latency_alert(self): self.assertIn("InferenceLatencySLOBreach",evaluate(self.rows("latency_breach"))["alerts"])
 def test_degenerate_alert(self): self.assertIn("DegenerateScoreDistribution",evaluate(self.rows("degenerate_quality_breach"))["alerts"])
if __name__=="__main__": unittest.main()
