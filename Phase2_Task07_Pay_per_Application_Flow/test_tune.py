import unittest
from tune import evaluate
R=[{"item_id":"a","relevance_score":1,"conversion_score":0,"relevant":1,"converted":0},{"item_id":"b","relevance_score":0,"conversion_score":1,"relevant":0,"converted":1},{"item_id":"c","relevance_score":.5,"conversion_score":.5,"relevant":1,"converted":1}]
class Tests(unittest.TestCase):
 def test_relevance_weight(self): self.assertEqual(evaluate(R,1)["top_items"][0],"a")
 def test_conversion_weight(self): self.assertEqual(evaluate(R,0)["top_items"][0],"b")
if __name__=="__main__": unittest.main()
