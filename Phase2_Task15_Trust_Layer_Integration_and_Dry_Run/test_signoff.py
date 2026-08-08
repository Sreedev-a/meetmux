import unittest
from signoff import evaluate
E={"parser":{"coverage":.95,"unresolved_rate":.05},"proctor":{"hardened_fp":0,"baseline_fp":2,"recall":1},"operations":{"rollback_owner":"owner","artifacts_verified":[True]}}
class Tests(unittest.TestCase):
 def test_pass(self): self.assertTrue(evaluate(E)["signed_off"])
 def test_fail_closed(self):
  x={**E,"proctor":{**E["proctor"],"recall":.5}}; self.assertFalse(evaluate(x)["signed_off"])
if __name__=="__main__": unittest.main()
