import csv,json
from pathlib import Path
ROOT=Path(__file__).parent
def evaluate(rows,weight):
 ranked=sorted(rows,key=lambda r:-(weight*float(r["relevance_score"])+(1-weight)*float(r["conversion_score"])))[:3]
 return {"weight":weight,"precision_at_3":sum(int(r["relevant"]) for r in ranked)/3,"conversion_at_3":sum(int(r["converted"]) for r in ranked)/3,"top_items":[r["item_id"] for r in ranked]}
def main():
 rows=list(csv.DictReader((ROOT/"data/tuning_labels.csv").open())); trials=[evaluate(rows,w) for w in [0,.2,.4,.6,.8,1]]; feasible=[x for x in trials if x["precision_at_3"]>=2/3]; best=max(feasible,key=lambda x:(x["conversion_at_3"],x["precision_at_3"],x["weight"])); report={"objective":"maximize conversion_at_3 with precision_at_3 >= 0.6667","trials":trials,"selected":best}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/tuning_report.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(best,indent=2))
if __name__=="__main__": main()
