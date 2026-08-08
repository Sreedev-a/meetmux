import unittest
from guardrail import assess
class Tests(unittest.TestCase):
 def test_good_fit(self): self.assertFalse(assess({"application_id":"a","match_score":.8})["warning"])
 def test_low_fit(self):
  x=assess({"application_id":"a","match_score":.4,"skill_gaps":["sql"]}); self.assertEqual(x["severity"],"high"); self.assertTrue(x["requires_acknowledgement"])
if __name__=="__main__": unittest.main()
