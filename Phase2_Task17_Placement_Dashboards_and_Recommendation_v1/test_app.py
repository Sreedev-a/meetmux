import unittest
from app import create_app,recommend
class Tests(unittest.TestCase):
 def test_rank(self): self.assertEqual(recommend({"skills":{"python":90,"sql":80},"experience":2,"locations":["Bengaluru"],"modes":["hybrid"]})[0]["job_id"],"j1")
 def test_filters(self): self.assertEqual({x["job_id"] for x in recommend({})},{"j1","j2"})
 def test_validation(self): self.assertEqual(create_app().test_client().post("/v1/recommendations/jobs",json={"limit":99}).status_code,422)
if __name__=="__main__": unittest.main()
