from .eligibility import eligible_jobs
def rank_baseline(candidate,jobs,k,today=None):
 return sorted(eligible_jobs(candidate,jobs,today),key=lambda j:(-j.popularity,-j.quality,j.posted_days_ago,j.job_id))[:k]
