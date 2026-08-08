import csv,json,math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent
def metrics(rows,k=3):
 ranked=sorted(rows,key=lambda x:-float(x["score"])); rel=[int(x["relevant"]) for x in ranked]; dcg=sum(r/math.log2(i+2) for i,r in enumerate(rel[:k])); ideal=sorted(rel,reverse=True); idcg=sum(r/math.log2(i+2) for i,r in enumerate(ideal[:k])); total=sum(rel)
 return {"ndcg_at_3":round(dcg/idcg if idcg else 0,6),"precision_at_3":round(sum(rel[:k])/k,6),"recall_at_3":round(sum(rel[:k])/total if total else 0,6),"mrr":round(next((1/i for i,r in enumerate(rel,1) if r),0),6)}
def main():
 groups=defaultdict(list)
 with (ROOT/"data/labeled_impressions.csv").open() as f:
  for row in csv.DictReader(f): groups[row["query_id"]].append(row)
 per={q:metrics(r) for q,r in groups.items()}; agg={k:round(sum(x[k] for x in per.values())/len(per),6) for k in next(iter(per.values()))}; report={"baseline_version":"pre_paywall_v1","query_count":len(per),"per_query":per,"aggregate":agg}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/match_quality_baseline.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(agg,indent=2))
if __name__=="__main__": main()
