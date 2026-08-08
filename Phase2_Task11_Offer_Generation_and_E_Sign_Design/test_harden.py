import unittest
from harden import evaluate
R=[{"risk_score":.9,"violation":1},{"risk_score":.6,"violation":0},{"risk_score":.2,"violation":0}]
class Tests(unittest.TestCase):
 def test_confusion_counts(self):
  x=evaluate(R,.5); self.assertEqual((x["tp"],x["fp"],x["tn"],x["fn"]),(1,1,1,0))
if __name__=="__main__": unittest.main()
