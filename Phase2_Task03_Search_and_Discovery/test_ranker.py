import json, unittest
from pathlib import Path
from ranker import rank_jobs,rank_candidates
DATA=json.loads((Path(__file__).parent/"data/marketplace.json").read_text())
class Tests(unittest.TestCase):
 def test_job_ranking(self): self.assertEqual(rank_jobs(DATA["students"][0],DATA["jobs"])[0]["job_id"],"job_1")
 def test_candidate_ranking(self): self.assertEqual(rank_candidates(DATA["jobs"][0],DATA["students"])[0]["student_id"],"stu_1")
 def test_bounded(self): self.assertTrue(all(0<=x["score"]<=1 for x in rank_jobs(DATA["students"][0],DATA["jobs"])))
if __name__=="__main__": unittest.main()
