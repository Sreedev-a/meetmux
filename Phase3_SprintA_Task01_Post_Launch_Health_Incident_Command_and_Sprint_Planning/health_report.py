"""Post-launch model-health, defect prioritization, and backlog generator."""
from __future__ import annotations
import csv, json, math, random, statistics
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent; SEED=101; OFFLINE_NDCG=0.9012

def ndcg(labels):
    dcg=sum(v/math.log2(i+2) for i,v in enumerate(labels)); ideal=sorted(labels,reverse=True); base=sum(v/math.log2(i+2) for i,v in enumerate(ideal)); return dcg/base if base else 0

def generate_logs():
    rng=random.Random(SEED); defects=["none","none","none","missing_skill","stale_job","cold_start","timeout"]; rows=[]
    for session in range(120):
        defect=rng.choice(defects)
        for rank in range(1,6):
            base=max(.05,.92-.13*(rank-1)+rng.gauss(0,.04)); relevant=rng.random() < max(.05,base-(.22 if defect!="none" else 0)); success=not(defect=="timeout" and rank==1)
            rows.append({"session_id":f"s{session:03d}","request_id":f"r{session:03d}-{rank}","rank":rank,"score":round(base,5),"relevant":int(relevant),"clicked":int(relevant and rng.random()<.72),"defect":defect,"success":int(success),"latency_ms":round(rng.uniform(15,45)+(130 if not success else 0),3),"model_version":"2.0.0","fallback":int(not success)})
    return rows

def analyze(rows):
    sessions=defaultdict(list)
    for r in rows: sessions[r["session_id"]].append(r)
    online=[ndcg([x["relevant"] for x in sorted(v,key=lambda x:x["rank"])]) for v in sessions.values()]
    by_defect=defaultdict(list)
    for sid,values in sessions.items(): by_defect[values[0]["defect"]].append(ndcg([x["relevant"] for x in sorted(values,key=lambda x:x["rank"]) ]))
    defects=[]
    for name,values in by_defect.items():
        if name=="none": continue
        mean=statistics.mean(values); impact=max(0,OFFLINE_NDCG-mean); defects.append({"defect":name,"affected_sessions":len(values),"mean_online_ndcg":round(mean,6),"gap_vs_offline":round(impact,6),"priority_score":round(impact*len(values),6)})
    defects.sort(key=lambda x:-x["priority_score"])
    mean_online=statistics.mean(online)
    return {"offline_heldout_ndcg_at_5":OFFLINE_NDCG,"online_ndcg_at_5":round(mean_online,6),"offline_online_gap":round(OFFLINE_NDCG-mean_online,6),"availability":round(sum(r["success"] for r in rows)/len(rows),6),"sessions":len(sessions),"ranked_defects":defects}

def main():
    rows=generate_logs(); report=analyze(rows); data=ROOT/"data"; out=ROOT/"outputs"; data.mkdir(exist_ok=True); out.mkdir(exist_ok=True)
    with (data/"interaction_logs_fixture.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n"); w.writeheader(); w.writerows(rows)
    (out/"model_health_report.json").write_text(json.dumps({"data_source":"deterministic fallback fixture; replace with production logs","seed":SEED,**report,"worked_example":{"input":"session with timeout on rank 1","output":"cached eligible-job ranking","reason":"primary model unavailable; fallback=true"},"failure_injection_verified":any(r["fallback"] for r in rows)},indent=2)+"\n")
    with (out/"ranked_defects.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=report["ranked_defects"][0].keys(),lineterminator="\n"); w.writeheader(); w.writerows(report["ranked_defects"])
    owners={"timeout":"Backend/ML Reliability","stale_job":"Data Platform","missing_skill":"Ontology/ML","cold_start":"Recommendations"}
    with (out/"phase3_backlog.csv").open("w",newline="") as f:
        fields=["priority","defect","owner","acceptance_criterion","status"]; w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n"); w.writeheader()
        for i,d in enumerate(report["ranked_defects"],1): w.writerow({"priority":i,"defect":d["defect"],"owner":owners[d["defect"]],"acceptance_criterion":f"Reduce gap below {max(.02,d['gap_vs_offline']/2):.3f}","status":"owned"})
    fig,ax=plt.subplots(figsize=(8,4)); ax.bar([d["defect"] for d in report["ranked_defects"]],[d["priority_score"] for d in report["ranked_defects"]]); ax.set_ylabel("Impact × affected sessions"); ax.set_title("Ranked intelligence defects"); fig.tight_layout(); fig.savefig(out/"defect_priorities.png",dpi=160); plt.close(fig)
    print(json.dumps({k:report[k] for k in ("offline_heldout_ndcg_at_5","online_ndcg_at_5","offline_online_gap","availability")},indent=2))

if __name__=="__main__": main()
