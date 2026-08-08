import json
from pathlib import Path
ROOT=Path(__file__).parent
WEIGHTS={"skills":.7,"experience":.15,"location":.1,"work_mode":.05}
def explain(student,job):
 skills=[]
 for name,threshold in sorted(job["skills"].items()):
  actual=student["skills"].get(name,0); ratio=min(actual/threshold,1)
  skills.append({"skill":name,"verified_score":actual,"threshold":threshold,"met":actual>=threshold,"gap":max(threshold-actual,0)})
 parts={"skills":sum(min(x["verified_score"]/x["threshold"],1) for x in skills)/len(skills),"experience":min(student["experience"]/max(job["experience"],.1),1),"location":float(job["location"] in student["locations"]),"work_mode":float(job["work_mode"] in student["work_modes"])}
 contributions={k:round(parts[k]*WEIGHTS[k],4) for k in parts}; gaps=[x for x in skills if not x["met"]]
 return {"student_id":student["id"],"job_id":job["id"],"score":round(sum(contributions.values()),4),"eligible":not gaps,"contributions":contributions,"skill_evidence":skills,"strengths":[x["skill"] for x in skills if x["met"]],"gaps":[{"skill":x["skill"],"points_needed":x["gap"]} for x in gaps],"summary":f"Meets {len(skills)-len(gaps)} of {len(skills)} required skill thresholds."}
def main():
 d=json.loads((ROOT/"data/cases.json").read_text()); out=[explain(s,j) for s in d["students"] for j in d["jobs"]]; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/explained_matches.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"matches":len(out),"all_explained":all(x["contributions"] and x["summary"] for x in out)},indent=2))
if __name__=="__main__": main()
