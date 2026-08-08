import unittest
from analyze_items import analyze
class Tests(unittest.TestCase):
 def test_flags_too_easy(self):
  rows={"x":[{"correct":1,"total_score":i} for i in range(8)]}; self.assertIn("TOO_EASY",analyze(rows)[0]["flags"])
if __name__=="__main__": unittest.main()
