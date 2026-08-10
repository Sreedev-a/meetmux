from .baseline import rank_baseline
def fallback_jobs(candidate,jobs,k,today=None):
 popular=rank_baseline(candidate,jobs,k,today)
 if popular:return popular,1,"popular_fallback"
 active=sorted([j for j in jobs if j.active and (today is None or j.expires_on>=today)],key=lambda j:(j.posted_days_ago,j.job_id))[:k]
 return active,2,"recent_fallback" if active else "no_active_jobs"
