import unittest
from validate_design import validate
C={"version":"1","objective":"x","candidate_sources":[],"features":["a"],"weights":{"a":1},"hard_filters":[],"offline_metrics":[],"guardrails":[],"fallback":"x"}
class Tests(unittest.TestCase):
 def test_valid(self): self.assertFalse(validate(C))
 def test_bad_weights(self): self.assertIn("weights_sum:0.5",validate({**C,"weights":{"a":.5}}))
if __name__=="__main__": unittest.main()
