import unittest
from map_ontology import map_document
O={"version":"1","skills":[{"id":"s.sql","name":"sql","aliases":["postgresql"],"domain":"data"}]}
class Tests(unittest.TestCase):
 def test_alias(self): self.assertEqual(map_document({"id":"d","text":"PostgreSQL"},O)["mapped_skills"][0]["skill_id"],"s.sql")
 def test_unresolved(self): self.assertEqual(map_document({"id":"d","text":"#rust"},O)["unresolved_tags"],["#rust"])
if __name__=="__main__": unittest.main()
