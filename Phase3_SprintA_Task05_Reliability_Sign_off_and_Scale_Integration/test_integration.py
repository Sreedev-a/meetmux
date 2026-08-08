import unittest
from service import create_app,predict,reset_metrics,snapshot
class Tests(unittest.TestCase):
 def test_endpoint_and_monitoring(self):
  reset_metrics(); c=create_app().test_client(); r=c.post("/predict",json={"features":[.9,.8,.7]}); self.assertEqual(r.status_code,200); self.assertFalse(r.json["fallback"]); self.assertEqual(c.get("/metrics").json["requests"],1)
 def test_validation(self): self.assertEqual(create_app().test_client().post("/predict",json={"features":[1]}).status_code,422)
 def test_forced_failure(self):
  r=predict([.9,.8,.7],True); self.assertTrue(r["fallback"]); self.assertEqual(r["reason"],"injected_model_failure")
if __name__=="__main__": unittest.main()
