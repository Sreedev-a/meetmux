import unittest
from validate_recommendations import ndcg
class Tests(unittest.TestCase):
 def test_perfect(self): self.assertEqual(ndcg([1,1,0]),1)
 def test_bad_order(self): self.assertLess(ndcg([0,1,1]),1)
if __name__=="__main__": unittest.main()
