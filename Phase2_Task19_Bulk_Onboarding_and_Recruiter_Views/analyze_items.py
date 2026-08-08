import csv,json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent
def analyze(rows):
 out=[]
 for item,rs in sorted(rows.items()):
  rs=sorted(rs,key=lambda x:float(x["total_score"])); n=len(rs); q=max(1,n//4); difficulty=sum(int(x["correct"]) for x in rs)/n; discrimination=sum(int(x["correct"]) for x in rs[-q:])/q-sum(int(x["correct"]) for x in rs[:q])/q; reasons=[]
  if n<8: reasons.append("LOW_SAMPLE")
  if difficulty<.2: reasons.append("TOO_HARD")
  if difficulty>.9: reasons.append("TOO_EASY")
  if discrimination<.2: reasons.append("LOW_DISCRIMINATION")
  out.append({"item_id":item,"responses":n,"difficulty":round(difficulty,4),"discrimination":round(discrimination,4),"weak_item":bool(reasons),"flags":reasons})
 return out
def main():
 groups=defaultdict(list)
 with (ROOT/"data/responses.csv").open() as f:
  for r in csv.DictReader(f): groups[r["item_id"]].append(r)
 out=analyze(groups); folder=ROOT/"outputs"; folder.mkdir(exist_ok=True); (folder/"item_quality_flags.json").write_text(json.dumps(out,indent=2)+"\n");
 with (folder/"item_quality_flags.csv").open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=["item_id","responses","difficulty","discrimination","weak_item","flags"]); w.writeheader(); w.writerows({**x,"flags":"|".join(x["flags"])} for x in out)
 print(json.dumps({"items":len(out),"weak_items":sum(x["weak_item"] for x in out)},indent=2))
if __name__=="__main__": main()
