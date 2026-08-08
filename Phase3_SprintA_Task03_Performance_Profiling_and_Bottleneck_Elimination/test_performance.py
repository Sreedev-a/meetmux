import unittest
from profile_optimize import baseline,catalog,optimized,prepare,safe_predict
class Tests(unittest.TestCase):
 def test_exact_equivalence(self):
  jobs=catalog(30); q=list(range(1,13)); self.assertEqual(baseline(q,jobs),optimized(q,prepare(jobs)))
 def test_unavailable_fallback(self): self.assertTrue(safe_predict(list(range(1,13)),prepare(catalog(30)),False)["fallback"])
if __name__=="__main__": unittest.main()
