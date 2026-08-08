import unittest
from load_test import Service,run_level
class Tests(unittest.TestCase):
 def test_target_healthy(self): self.assertTrue(run_level(4,3)["slo_pass"])
 def test_overload_fallback(self):
  result=run_level(16,3); self.assertGreater(result["fallback_rate"],0); self.assertFalse(result["slo_pass"])
 def test_unavailable_contract(self): self.assertIn("fallback",Service().predict([.5]*12))
if __name__=="__main__": unittest.main()
