import json
from pathlib import Path
ROOT=Path(__file__).parent; W={"skill_fit":.65,"experience_fit":.15,"location_fit":.1,"work_mode_fit":.1}
def explain(s,j):
 evidence=[]
 for skill,threshold in j["skills"].items():
  actual=s["skills"].get(skill,0); evidence.append({"skill":skill,"actual":actual,"required":threshold,"gap":max(threshold-actual,0)})
 parts={"skill_fit":sum(min(x["actual"]/x["required"],1) for x in evidence)/len(evidence),"experience_fit":min(s["experience"]/max(j["experience"],.1),1),"location_fit":float(j["location"] in s["locations"]),"work_mode_fit":float(j["mode"] in s["modes"])}; contrib={k:round(parts[k]*W[k],4) for k in parts}; ordered=sorted(contrib,key=contrib.get,reverse=True); gaps=[x for x in evidence if x["gap"]>0]; actions=[f"Improve {x['skill']} by {x['gap']} points to meet the threshold." for x in sorted(gaps,key=lambda x:-x["gap"])];
 if not parts["location_fit"]: actions.append(f"Add {j['location']} to preferred locations.")
 if not parts["work_mode_fit"]: actions.append(f"Accept {j['mode']} work mode.")
 return {"student_id":s["id"],"job_id":j["id"],"score":round(sum(contrib.values()),4),"feature_values":parts,"weighted_contributions":contrib,"strongest_factors":ordered[:2],"limiting_factors":[k for k in ordered if parts[k]<1],"skill_evidence":evidence,"next_best_actions":actions[:3],"explanation_version":"2.0.0"}
def main():
 d=json.loads((ROOT/"data/cases.json").read_text()); out=[explain(x["student"],x["job"]) for x in d]; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/rich_explanations.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"recommendations":len(out),"actionable":sum(bool(x["next_best_actions"]) for x in out)},indent=2))
if __name__=="__main__": main()
