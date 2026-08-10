from uuid import uuid4
from .candidate_features import normalize,normalized_scores
from .eligibility import eligible_jobs
from .exploration import select_exploration
from .fallback import fallback_jobs
from .job_features import normalized_requirements
from .schemas import ColdStartResponse,Recommendation,Source

WEIGHTS={"skills":.5,"role":.18,"location":.12,"experience":.08,"quality":.07,"freshness":.05}
def score_job(candidate,job):
 scores=normalized_scores(candidate.verified_scores); req=normalized_requirements(job)
 skill=sum(min(scores.get(s,0)/max(t,.01),1) for s,t in req.items())/len(req) if req else .5
 role=float(normalize(job.role_family) in {normalize(x) for x in candidate.preferred_roles}) if candidate.preferred_roles else .5
 loc=float(job.remote or normalize(job.location) in {normalize(x) for x in candidate.preferred_locations}) if candidate.preferred_locations else .5
 exp=float(candidate.experience_level==job.experience_level); fresh=max(0,1-job.posted_days_ago/30)
 total=WEIGHTS["skills"]*skill+WEIGHTS["role"]*role+WEIGHTS["location"]*loc+WEIGHTS["experience"]*exp+WEIGHTS["quality"]*job.quality+WEIGHTS["freshness"]*fresh
 matched=sorted(s for s,t in req.items() if scores.get(s,0)>=t); gaps=sorted(s for s,t in req.items() if scores.get(s,0)<t)
 return min(1,total),matched,gaps,bool(role),bool(loc)
def recommend(candidate,jobs,k=5,exploration_fraction=.2,force_failure=False,today=None):
 try:
  if force_failure: raise RuntimeError("forced_model_failure")
  pool=eligible_jobs(candidate,jobs,today)
  ranked=sorted([(score_job(candidate,j),j) for j in pool],key=lambda x:(-x[0][0],x[1].job_id))
  if not ranked: raise RuntimeError("no_eligible_jobs")
  explore_count=min(round(k*exploration_fraction),max(0,len(ranked)-1)); explored=select_exploration([j for _,j in ranked],explore_count)
  chosen=[j for _,j in ranked if j not in explored][:max(0,k-len(explored))]+explored
  fallback_used=False;tier=None;model="cold-start-v1";reason=None
 except RuntimeError as exc:
  chosen,tier,source=fallback_jobs(candidate,jobs,k,today); fallback_used=True;model="cold-start-fallback-v1";reason=str(exc);explored=[]
 recs=[]
 for position,j in enumerate(chosen[:k],1):
  score,matched,gaps,role,loc=score_job(candidate,j)
  source=Source.EXPLORATION if j in explored else (Source.POPULAR if fallback_used and tier==1 else Source.RECENT if fallback_used else Source.PERSONALIZED)
  evidence=[]
  if matched:evidence.append("verified "+", ".join(matched)+" meet requirements")
  if role:evidence.append("role preference matches")
  if loc:evidence.append("location preference matches")
  if not evidence:evidence.append("eligible quality job for profile discovery")
  recs.append(Recommendation(job_id=j.job_id,position=position,score=round(score,4),source=source,exploration=j in explored,reason="Recommended because "+"; ".join(evidence)+".",matched_skills=matched,skill_gaps=gaps))
 return ColdStartResponse(candidate_id=candidate.candidate_id,ranking_id="rank_"+uuid4().hex,model_name="cold_start_ranker" if not fallback_used else "cold_start_fallback",model_version=model,fallback_used=fallback_used,fallback_tier=tier,reason=reason,recommendations=recs)
