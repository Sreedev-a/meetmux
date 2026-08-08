import unittest
from explain_recommendation import explain
S={"id":"s","skills":{"python":60},"experience":0,"locations":[],"modes":[]}; J={"id":"j","skills":{"python":70},"experience":1,"location":"Pune","mode":"remote"}
class Tests(unittest.TestCase):
 def test_actionable_gap(self): self.assertIn("10 points",explain(S,J)["next_best_actions"][0])
 def test_score_sum(self):
  x=explain(S,J); self.assertAlmostEqual(x["score"],sum(x["weighted_contributions"].values()))
if __name__=="__main__": unittest.main()
