import unittest
class Tests(unittest.TestCase):
 def test_gate_examples(self):
  tolerance=-.02; self.assertTrue(-.01>=tolerance); self.assertFalse(-.03>=tolerance)
if __name__=="__main__": unittest.main()
