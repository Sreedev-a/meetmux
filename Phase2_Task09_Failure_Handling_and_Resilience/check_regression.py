import csv,json,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent; TOLERANCE=-.02
def main():
 rows=list(csv.DictReader((ROOT/"data/pre_post_quality.csv").open())); segments=defaultdict(list)
 for r in rows: segments[r["segment"]].append(float(r["post_ndcg"])-float(r["pre_ndcg"]))
 deltas=[float(r["post_ndcg"])-float(r["pre_ndcg"]) for r in rows]; by={k:round(statistics.mean(v),6) for k,v in segments.items()}; overall=round(statistics.mean(deltas),6); passed=overall>=TOLERANCE and all(v>=TOLERANCE for v in by.values())
 report={"metric":"NDCG@3","queries":len(rows),"allowed_delta":TOLERANCE,"mean_pre":round(statistics.mean(float(r["pre_ndcg"]) for r in rows),6),"mean_post":round(statistics.mean(float(r["post_ndcg"]) for r in rows),6),"mean_delta":overall,"segment_deltas":by,"relevance_regression":not passed,"release_decision":"pass" if passed else "rollback"}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/conversion_quality_check.json").write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); assert passed
if __name__=="__main__": main()
