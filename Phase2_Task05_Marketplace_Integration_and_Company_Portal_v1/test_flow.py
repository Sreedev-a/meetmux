import unittest
from validate_flow import match
class Tests(unittest.TestCase):
 def test_eligible(self): self.assertTrue(match({"skills":{"python":80},"modes":["remote"]},{"id":"j","skills":{"python":70},"mode":"remote"})["eligible"])
 def test_explains_gap(self): self.assertEqual(match({"skills":{},"modes":[]},{"id":"j","skills":{"python":70},"mode":"remote"})["explanation"]["gaps"]["python"],70)
if __name__=="__main__": unittest.main()
