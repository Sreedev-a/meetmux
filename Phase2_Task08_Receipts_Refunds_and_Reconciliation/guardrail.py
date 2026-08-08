import json
from pathlib import Path
ROOT=Path(__file__).parent; WARN=.70; BLOCK=.45
def assess(application):
 score=float(application["match_score"]); gaps=application.get("skill_gaps",[]); level="high" if score<BLOCK else "medium" if score<WARN else "none"
 return {"application_id":application["application_id"],"warning":level!="none","severity":level,"match_score":score,"policy":{"warning_below":WARN,"high_risk_below":BLOCK},"reasons":([f"match score {score:.2f} is below {WARN:.2f}"] if score<WARN else [])+([f"missing threshold: {x}" for x in gaps]),"requires_acknowledgement":level!="none","action":"allow_with_acknowledgement" if level!="none" else "allow"}
def main():
 apps=json.loads((ROOT/"data/applications.json").read_text()); out=[assess(x) for x in apps]; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/spend_quality_warnings.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"applications":len(out),"warnings":sum(x["warning"] for x in out),"high_risk":sum(x["severity"]=="high" for x in out)},indent=2))
if __name__=="__main__": main()
