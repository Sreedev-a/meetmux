import unittest
from parser_v0 import parse
class Tests(unittest.TestCase):
 def test_aliases(self): self.assertEqual([x["canonical_skill"] for x in parse({"id":"x","type":"resume","text":"Python3 and PostgreSQL"})["skills"]],["python","sql"])
 def test_years(self): self.assertEqual(parse({"id":"x","type":"resume","text":"3+ years Python"})["years_experience"],3)
 def test_word_boundary(self): self.assertFalse(parse({"id":"x","type":"resume","text":"pythonic"})["skills"])
if __name__=="__main__": unittest.main()
