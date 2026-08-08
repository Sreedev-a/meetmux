import csv,json
from pathlib import Path
ROOT=Path(__file__).parent
def evaluate(rows,t):
 y=[int(r["violation"]) for r in rows]; p=[float(r["risk_score"])>=t for r in rows]; tp=sum(a and b for a,b in zip(y,p)); fp=sum(not a and b for a,b in zip(y,p)); tn=sum(not a and not b for a,b in zip(y,p)); fn=sum(a and not b for a,b in zip(y,p)); return {"threshold":t,"false_positive_rate":round(fp/(fp+tn),4),"recall":round(tp/(tp+fn),4),"tp":tp,"fp":fp,"tn":tn,"fn":fn}
def main():
 rows=list(csv.DictReader((ROOT/"data/proctor_events.csv").open())); baseline=evaluate(rows,.5); trials=[evaluate(rows,t) for t in [.5,.55,.6,.65,.7,.75]]; candidate=min((x for x in trials if x["recall"]>=.8),key=lambda x:(x["false_positive_rate"],-x["recall"])); report={"stage":"hardening_start","baseline":baseline,"threshold_trials":trials,"candidate":candidate,"relative_fp_reduction":round((baseline["false_positive_rate"]-candidate["false_positive_rate"])/baseline["false_positive_rate"],4)}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/hardening_report.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
