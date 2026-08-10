import json,os
from collections import Counter
from datetime import date,datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent
os.environ.setdefault("MPLBACKEND","Agg");os.environ.setdefault("MPLCONFIGDIR",str(ROOT/".matplotlib"))
import matplotlib.pyplot as plt
from src.cold_start import recommend
from src.demo_data import fresh_candidate,jobs
from src.evaluator import evaluate
from src.instrumentation import log_response
from src.metrics import absolute_lift,fallback_rate,non_empty_rate,relative_lift
from src.schemas import CandidateProfile
def plot(summary):
 out=ROOT/"outputs";out.mkdir(exist_ok=True)
 ev=summary["evaluation"]
 fig,ax=plt.subplots(figsize=(8,5));names=["NDCG@5","Recall@5","Precision@5","MRR"];x=range(4);ax.bar([i-.18 for i in x],[ev["baseline"][k] for k in ["ndcg_at_5","recall_at_5","precision_at_5","mrr"]],.36,label="Popularity baseline");ax.bar([i+.18 for i in x],[ev["cold_start"][k] for k in ["ndcg_at_5","recall_at_5","precision_at_5","mrr"]],.36,label="Cold start");ax.set_xticks(list(x),names);ax.set_ylim(0,1.1);ax.set(title="Controlled Offline Fixture: Baseline vs Cold Start",ylabel="Metric");ax.legend();fig.tight_layout();fig.savefig(out/"baseline_vs_cold_start.png",dpi=180);plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4));ax.text(.5,.5,"No genuine first-session action data available\nProduction A/B test required",ha="center",va="center",fontsize=14);ax.axis("off");ax.set_title("First-Session Action Rates: Not Available");fig.tight_layout();fig.savefig(out/"first_session_action_rates.png",dpi=180);plt.close(fig)
 per=ev["per_candidate"];fig,ax=plt.subplots(figsize=(8,4.5));ax.plot(range(1,6),[sum(r["cold_start"][p-1] in set(r["relevant"]) for r in per)/len(per) for p in range(1,6)],marker="o");ax.set(title="Controlled Relevance Rate by Position",xlabel="Position",ylabel="Relevant share",ylim=(0,1));fig.tight_layout();fig.savefig(out/"relevance_by_position.png",dpi=180);plt.close(fig)
 fallback=summary["profile_coverage"];fig,ax=plt.subplots(figsize=(9,4.5));bars=ax.bar([x["profile"] for x in fallback],[x["count"] for x in fallback]);ax.bar_label(bars);ax.tick_params(axis="x",rotation=25);ax.set(title="Recommendation Count Across Profile/Failure Cases",ylabel="Recommendations");fig.tight_layout();fig.savefig(out/"fallback_coverage.png",dpi=180);plt.close(fig)
 mix=summary["source_mix"];fig,ax=plt.subplots(figsize=(7,4.5));bars=ax.bar(list(mix),list(mix.values()));ax.bar_label(bars);ax.set(title="Runtime Recommendation Source Mix",ylabel="Recommendations");fig.tight_layout();fig.savefig(out/"recommendation_source_mix.png",dpi=180);plt.close(fig)
def main():
 inventory=jobs();candidate=fresh_candidate();primary=recommend(candidate,inventory,5,.2,today=date(2026,8,10));baseline_ids=[x.job_id for x in __import__("src.baseline",fromlist=["rank_baseline"]).rank_baseline(candidate,inventory,5,date(2026,8,10))]
 log=ROOT/"data/runtime_evidence/cold_start_impressions.jsonl";log.unlink(missing_ok=True);events=log_response(primary,candidate.candidate_id,REPO,log)
 failure=recommend(candidate,inventory,5,.2,True,date(2026,8,10))
 profiles=[("rich",candidate),("partial",CandidateProfile(candidate_id="partial",verified_scores={"python":.7})),("scores_only",CandidateProfile(candidate_id="scores",verified_scores={"sql":.7})),("role_only",CandidateProfile(candidate_id="role",preferred_roles=["data_analysis"])),("minimal",CandidateProfile(candidate_id="minimal")),("unknown_skill",CandidateProfile(candidate_id="unknown",verified_scores={"quantum_widgets":.9}))]
 responses=[recommend(c,inventory,5,.2,today=date(2026,8,10)) for _,c in profiles]+[failure];coverage=[{"profile":name,"count":len(r.recommendations),"fallback":r.fallback_used,"tier":r.fallback_tier} for (name,_),r in zip(profiles,responses)]+[{"profile":"forced_failure","count":len(failure.recommendations),"fallback":True,"tier":failure.fallback_tier}]
 evaluation=evaluate(inventory);mix=Counter(r.source.value for response in responses for r in response.recommendations)
 summary={"data_provenance":"controlled runtime candidate/job inventory; repository has no genuine first-session outcomes","fresh_candidate":{"candidate_id":candidate.candidate_id,"interaction_count":candidate.interaction_count,"onboarding":candidate.model_dump(mode="json")},"inventory_jobs":len(inventory),"active_unexpired_jobs":10,"k":5,"exploration_fraction":.2,"baseline_ids":baseline_ids,"primary_response":primary.model_dump(mode="json"),"task6_impressions":len(events),"failure_response":failure.model_dump(mode="json"),"profile_coverage":coverage,"non_empty_rate":non_empty_rate(responses),"fallback_rate":fallback_rate(responses),"source_mix":dict(mix),"evaluation":evaluation,"offline_ndcg_absolute_lift":absolute_lift(evaluation["baseline"]["ndcg_at_5"],evaluation["cold_start"]["ndcg_at_5"]),"offline_ndcg_relative_lift":relative_lift(evaluation["baseline"]["ndcg_at_5"],evaluation["cold_start"]["ndcg_at_5"]),"online_action_lift":None,"run":{"run_id":"cold_start_controlled_v1","timestamp":datetime.now(timezone.utc).isoformat(),"random_seed":42,"model_version":"cold-start-v1","weights":{"skills":.5,"role":.18,"location":.12,"experience":.08,"quality":.07,"freshness":.05}}}
 (ROOT/"data/runtime_evidence/summary.json").write_text(json.dumps(summary,indent=2)+"\n");(ROOT/"reports/experiment_log.json").write_text(json.dumps(summary["run"]|{"dataset":"controlled runtime fixture","evaluation_split":"four held-out fixture candidates; no tuning","k":5,"exploration_fraction":.2,"metrics":evaluation,"online_action_lift":None},indent=2)+"\n")
 top=primary.recommendations[0];(ROOT/"reports/E2E_FRESH_CANDIDATE_TRACE.md").write_text(f"# Fresh Candidate Runtime Trace\n\nCandidate `{candidate.candidate_id}` was created as an equivalent fresh profile because no account service exists. Prior interaction count: **{candidate.interaction_count}**. Onboarding supplied verified Python 0.88, SQL 0.76 and ML 0.71 plus role/location preferences.\n\nThe API/service returned {len(primary.recommendations)} jobs under ranking `{primary.ranking_id}`, model `{primary.model_version}`, fallback `{primary.fallback_used}`. Top result `{top.job_id}` scored {top.score:.4f} at position {top.position}, source `{top.source.value}`, impression `{top.impression_id}`: {top.reason}\n\nAll {len(events)} impressions were emitted using Task 6's exact schema/logger. No click/apply/shortlist outcome is shown because none genuinely occurred.\n")
 plot(summary);print(json.dumps(summary,indent=2));return summary
if __name__=="__main__":main()
