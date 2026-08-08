import csv,json,statistics
from datetime import datetime,timezone
from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).parent; SEED=42
def load(name):
 with (ROOT/"data"/name).open() as f: return list(csv.DictReader(f))
def standardized_mean_shift(ref,cur,feature):
 a=[float(x[feature]) for x in ref]; b=[float(x[feature]) for x in cur]; sd=statistics.pstdev(a) or 1; return abs(statistics.mean(b)-statistics.mean(a))/sd
def main():
 ref,cur=load("reference.csv"),load("current.csv"); features=["skill_fit","experience_fit"]; shifts={f:round(standardized_mean_shift(ref,cur,f),4) for f in features}; triggered=any(x>.5 for x in shifts.values()); report={"checked_at_utc":datetime.now(timezone.utc).isoformat(),"method":"absolute standardized mean shift","threshold":.5,"feature_shifts":shifts,"drift_detected":triggered,"retraining":None}
 if triggered:
  rows=ref+cur; X=[[float(r[f]) for f in features] for r in rows]; y=[int(r["selected"]) for r in rows]; xt,xv,yt,yv=train_test_split(X,y,test_size=.3,random_state=SEED,stratify=y); model=LogisticRegression(random_state=SEED).fit(xt,yt); acc=accuracy_score(yv,model.predict(xv)); promoted=acc>=.75; report["retraining"]={"validation_accuracy":round(acc,4),"promotion_threshold":.75,"promoted":promoted,"version":"2.0.0"}
  if promoted:
   (ROOT/"artifacts").mkdir(exist_ok=True); joblib.dump(model,ROOT/"artifacts/recommendation_gate_v2.0.0.joblib"); (ROOT/"artifacts/metadata.json").write_text(json.dumps({"version":"2.0.0","features":features,"seed":SEED,"validation_accuracy":round(acc,4)},indent=2)+"\n")
 (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/drift_retraining_report.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
