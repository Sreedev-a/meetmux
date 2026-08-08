import csv,json,math,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent
def ndcg(rels,k=3):
 dcg=sum(r/math.log2(i+2) for i,r in enumerate(rels[:k])); ideal=sorted(rels,reverse=True); base=sum(r/math.log2(i+2) for i,r in enumerate(ideal[:k])); return dcg/base if base else 0
def main():
 groups=defaultdict(list); segments={}
 with (ROOT/"data/recommendation_labels.csv").open() as f:
  for r in csv.DictReader(f): groups[r["user_id"]].append(r); segments[r["user_id"]]=r["segment"]
 per=[]
 for u,rows in groups.items():
  rows=sorted(rows,key=lambda r:int(r["rank"])); rel=[int(r["relevant"]) for r in rows]; per.append({"user_id":u,"segment":segments[u],"ndcg_at_3":round(ndcg(rel),4),"recall_at_3":round(sum(rel[:3])/sum(rel) if sum(rel) else 0,4),"results":len(rows)})
 seg={s:round(statistics.mean(x["ndcg_at_3"] for x in per if x["segment"]==s),4) for s in sorted(set(segments.values()))}; aggregate={"ndcg_at_3":round(statistics.mean(x["ndcg_at_3"] for x in per),4),"recall_at_3":round(statistics.mean(x["recall_at_3"] for x in per),4),"coverage":round(sum(x["results"]>0 for x in per)/len(per),4),"empty_result_rate":round(sum(x["results"]==0 for x in per)/len(per),4)}; gates={"ndcg>=0.75":aggregate["ndcg_at_3"]>=.75,"recall>=0.75":aggregate["recall_at_3"]>=.75,"coverage>=0.95":aggregate["coverage"]>=.95,"segments>=0.70":all(x>=.7 for x in seg.values())}; report={"per_user":per,"segments":seg,"aggregate":aggregate,"gates":gates,"validated":all(gates.values())}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/recommendation_validation.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps({"aggregate":aggregate,"gates":gates,"validated":report["validated"]},indent=2)); assert report["validated"]
if __name__=="__main__": main()
