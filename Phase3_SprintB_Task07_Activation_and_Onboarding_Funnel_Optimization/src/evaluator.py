from datetime import date
from .baseline import rank_baseline
from .cold_start import recommend
from .metrics import mrr,ndcg_at_k,precision_at_k,recall_at_k
from .schemas import CandidateProfile
def controlled_cases():
 return [(CandidateProfile(candidate_id="eval_ml",verified_scores={"python":.85,"ml":.75},preferred_roles=["machine_learning"],preferred_locations=["Remote"]),{"job_01","job_08","job_04"}),(CandidateProfile(candidate_id="eval_data",verified_scores={"sql":.82,"python":.65},preferred_roles=["data_analysis"],preferred_locations=["Pune"]),{"job_02","job_10"}),(CandidateProfile(candidate_id="eval_backend",verified_scores={"python":.8},preferred_roles=["backend"],preferred_locations=["Remote"]),{"job_03"}),(CandidateProfile(candidate_id="eval_engineer",verified_scores={"python":.75,"sql":.78},preferred_roles=["data_engineering"],preferred_locations=["Remote"]),{"job_06"})]
def evaluate(jobs,k=5):
 rows=[]
 for candidate,relevant in controlled_cases():
  baseline=[j.job_id for j in rank_baseline(candidate,jobs,k,date(2026,8,10))];cold=[r.job_id for r in recommend(candidate,jobs,k,.2,today=date(2026,8,10)).recommendations]
  rows.append({"candidate_id":candidate.candidate_id,"baseline":baseline,"cold_start":cold,"relevant":sorted(relevant),"baseline_ndcg":ndcg_at_k(baseline,relevant,k),"cold_start_ndcg":ndcg_at_k(cold,relevant,k),"baseline_recall":recall_at_k(baseline,relevant,k),"cold_start_recall":recall_at_k(cold,relevant,k),"baseline_precision":precision_at_k(baseline,relevant,k),"cold_start_precision":precision_at_k(cold,relevant,k),"baseline_mrr":mrr(baseline,relevant),"cold_start_mrr":mrr(cold,relevant)})
 def avg(key):return sum(r[key] for r in rows)/len(rows)
 return {"method":"controlled held-out engineering fixture; no training/tuning and no behavioural outcomes","users":len(rows),"jobs":len(jobs),"k":k,"per_candidate":rows,"baseline":{"ndcg_at_5":avg("baseline_ndcg"),"recall_at_5":avg("baseline_recall"),"precision_at_5":avg("baseline_precision"),"mrr":avg("baseline_mrr")},"cold_start":{"ndcg_at_5":avg("cold_start_ndcg"),"recall_at_5":avg("cold_start_recall"),"precision_at_5":avg("cold_start_precision"),"mrr":avg("cold_start_mrr")}}
