import unittest
from drift_retrain import standardized_mean_shift
class Tests(unittest.TestCase):
 def test_no_shift(self):
  r=[{"x":1},{"x":2}]; self.assertEqual(standardized_mean_shift(r,r,"x"),0)
 def test_shift(self):
  self.assertGreater(standardized_mean_shift([{"x":1},{"x":2}],[{"x":3},{"x":4}],"x"),.5)
if __name__=="__main__": unittest.main()
