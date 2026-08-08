import unittest
from explain import explain
S={"id":"s","skills":{"python":80,"sql":60},"experience":1,"locations":["Pune"],"work_modes":["remote"]}; J={"id":"j","skills":{"python":70,"sql":70},"experience":1,"location":"Pune","work_mode":"remote"}
class Tests(unittest.TestCase):
 def test_gap(self): self.assertEqual(explain(S,J)["gaps"],[{"skill":"sql","points_needed":10}])
 def test_sum(self):
  x=explain(S,J); self.assertAlmostEqual(x["score"],sum(x["contributions"].values()))
if __name__=="__main__": unittest.main()
