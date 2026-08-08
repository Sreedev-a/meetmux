import unittest
from fairness_audit import audit
class Tests(unittest.TestCase):
 def test_rates(self):
  r=[{"g":"a","selected":1,"qualified":1,"score":.8},{"g":"a","selected":0,"qualified":1,"score":.6}]; self.assertEqual(audit(r,"g")["a"]["selection_rate"],.5)
if __name__=="__main__": unittest.main()
