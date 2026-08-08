import json
from pathlib import Path
ROOT=Path(__file__).parent; REQUIRED={"version","objective","candidate_sources","features","weights","hard_filters","offline_metrics","guardrails","fallback"}
def validate(c):
 errors=[]; errors+=sorted(f"missing:{x}" for x in REQUIRED-set(c)); total=sum(c.get("weights",{}).values());
 if abs(total-1)>1e-9: errors.append(f"weights_sum:{total}")
 if set(c.get("weights",{}))!=set(c.get("features",[])): errors.append("feature_weight_mismatch")
 return errors
def main():
 c=json.loads((ROOT/"config/recommendation_v1.json").read_text()); errors=validate(c); report={"design_version":c["version"],"valid":not errors,"errors":errors,"components":sorted(REQUIRED),"rollout":"shadow -> 10% -> 50% -> 100% with guardrail gates"}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/design_validation.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); assert not errors
if __name__=="__main__": main()
