import csv,json
from pathlib import Path
ROOT=Path(__file__).parent
def metric(rows,t):
 truth=[int(r["violation"]) for r in rows]; pred=[float(r["risk_score"])>=t for r in rows]; tp=sum(a and b for a,b in zip(truth,pred)); fp=sum(not a and b for a,b in zip(truth,pred)); tn=sum(not a and not b for a,b in zip(truth,pred)); fn=sum(a and not b for a,b in zip(truth,pred)); return {"threshold":t,"tp":tp,"fp":fp,"tn":tn,"fn":fn,"false_positive_rate":round(fp/(fp+tn),4),"recall":round(tp/(tp+fn),4)}
def main():
 rows=list(csv.DictReader((ROOT/"data/holdout_events.csv").open())); before=metric(rows,.5); after=metric(rows,.6); passed=after["fp"]<before["fp"] and after["recall"]>=.8; report={"dataset":"unseen_holdout_v1","baseline":before,"hardened":after,"false_positives_reduced_by":before["fp"]-after["fp"],"acceptance":{"fp_strictly_lower":after["fp"]<before["fp"],"recall_at_least_0_8":after["recall"]>=.8},"passed":passed}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/fp_validation.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); assert passed
if __name__=="__main__": main()
