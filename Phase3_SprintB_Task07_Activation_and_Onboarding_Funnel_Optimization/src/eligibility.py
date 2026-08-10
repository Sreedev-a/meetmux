from datetime import date
from .schemas import CandidateProfile,Job
LEVEL={"entry":0,"mid":1,"senior":2}
def eligible(candidate:CandidateProfile,job:Job,today:date|None=None)->bool:
 today=today or date.today()
 return job.active and job.expires_on>=today and LEVEL[candidate.experience_level.value]>=max(0,LEVEL[job.experience_level.value]-1)
def eligible_jobs(candidate,jobs,today=None): return [j for j in jobs if eligible(candidate,j,today)]
