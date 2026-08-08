import unittest
from mlops import point_in_time
R=[{"entity_id":"s","event_time":"2026-01-01","v":1},{"entity_id":"s","event_time":"2026-01-03","v":2}]
class Tests(unittest.TestCase):
 def test_point_in_time(self): self.assertEqual(point_in_time(R,"s","2026-01-02")["v"],1)
 def test_no_future_leakage(self): self.assertIsNone(point_in_time(R,"s","2025-12-01"))
if __name__=="__main__": unittest.main()
