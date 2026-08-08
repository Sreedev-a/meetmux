import unittest
from health_report import analyze, generate_logs, ndcg
class Tests(unittest.TestCase):
 def test_ndcg_perfect(self): self.assertEqual(ndcg([1,1,0]),1)
 def test_report_has_gap_and_defects(self):
  r=analyze(generate_logs()); self.assertGreater(r["offline_online_gap"],0); self.assertEqual(len(r["ranked_defects"]),4)
 def test_failure_fallback_logged(self): self.assertTrue(any(r["fallback"] for r in generate_logs()))
if __name__=="__main__": unittest.main()
