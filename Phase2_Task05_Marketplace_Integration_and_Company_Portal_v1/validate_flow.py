import json
from pathlib import Path
ROOT=Path(__file__).parent
def match(student,job):
 ratios={k:min(student["skills"].get(k,0)/v,1) for k,v in job["skills"].items()}; score=.8*sum(ratios.values())/len(ratios)+.2*float(job["mode"] in student["modes"]); gaps={k:round(job["skills"][k]-student["skills"].get(k,0),2) for k in ratios if student["skills"].get(k,0)<job["skills"][k]}; return {"job_id":job["id"],"score":round(score,4),"eligible":not gaps,"explanation":{"skill_attainment":ratios,"gaps":gaps}}
def main():
 d=json.loads((ROOT/"data/integration_cases.json").read_text()); results=[]
 for case in d:
  ranked=sorted([match(case["student"],j) for j in case["jobs"]],key=lambda x:(-x["score"],x["job_id"])); checks={"expected_top":ranked[0]["job_id"]==case["expected_top"],"scores_bounded":all(0<=x["score"]<=1 for x in ranked),"explanations_present":all(x["explanation"] for x in ranked)}; results.append({"case":case["name"],"passed":all(checks.values()),"checks":checks,"ranking":ranked})
 report={"cases":results,"passed":sum(x["passed"] for x in results),"total":len(results),"integration_valid":all(x["passed"] for x in results)}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/integration_report.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps({k:report[k] for k in ("passed","total","integration_valid")},indent=2)); assert report["integration_valid"]
if __name__=="__main__": main()
