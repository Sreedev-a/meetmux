import csv,json,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent
def audit(rows,group_field):
 groups=defaultdict(list)
 for r in rows: groups[r[group_field]].append(r)
 metrics={}
 for g,rs in groups.items():
  positives=[r for r in rs if int(r["qualified"])]; metrics[g]={"n":len(rs),"selection_rate":round(sum(int(r["selected"]) for r in rs)/len(rs),4),"mean_score":round(statistics.mean(float(r["score"]) for r in rs),4),"false_negative_rate":round(sum(int(r["qualified"]) and not int(r["selected"]) for r in rs)/len(positives) if positives else 0,4)}
 best=max(x["selection_rate"] for x in metrics.values());
 for x in metrics.values(): x["disparate_impact_ratio"]=round(x["selection_rate"]/best if best else 0,4); x["review_flag"]=x["disparate_impact_ratio"]<.8 or x["n"]<10
 return metrics
def main():
 rows=list(csv.DictReader((ROOT/"data/audit_sample.csv").open())); report={"status":"UNDERWAY","scope":"offline recommendation selection audit","limitations":["small synthetic sample","association is not causation","requires legal/domain review"],"by_region":audit(rows,"region"),"by_first_generation":audit(rows,"first_generation")}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/fairness_audit_start.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
