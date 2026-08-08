import unittest
from validate_fp_reduction import metric
class Tests(unittest.TestCase):
 def test_threshold_reduces_flags(self):
  r=[{"violation":0,"risk_score":.55},{"violation":1,"risk_score":.9}]; self.assertLess(metric(r,.6)["fp"],metric(r,.5)["fp"])
if __name__=="__main__": unittest.main()
