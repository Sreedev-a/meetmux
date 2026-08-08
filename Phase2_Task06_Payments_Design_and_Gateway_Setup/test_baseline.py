import unittest
from baseline import metrics
class Tests(unittest.TestCase):
 def test_perfect(self): self.assertEqual(metrics([{"score":1,"relevant":1},{"score":0,"relevant":0}])["ndcg_at_3"],1)
 def test_empty_relevance(self): self.assertEqual(metrics([{"score":1,"relevant":0}])["mrr"],0)
if __name__=="__main__": unittest.main()
