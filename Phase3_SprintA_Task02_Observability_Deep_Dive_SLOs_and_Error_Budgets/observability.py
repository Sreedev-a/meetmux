"""Compute intelligence SLOs, alerts, distribution health, and error budget."""
import csv,json,math,random,statistics
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
SLO={"p95_latency_ms":100.0,"availability":.995,"min_quality":.80,"min_score_stddev":.03,"owner":"ML Reliability Owner"}
def pctl(v,q):
 o=sorted(v); return o[min(len(o)-1,math.ceil(len(o)*q)-1)]
def evaluate(rows):
 scores=[float(r["score"]) for r in rows if int(r["success"])]; labeled=[r for r in rows if r["correct"]!=""]
 m={"requests":len(rows),"p95_latency_ms":round(pctl([float(r["latency_ms"]) for r in rows],.95),4),"availability":round(sum(int(r["success"]) for r in rows)/len(rows),6),"quality":round(sum(int(r["correct"]) for r in labeled)/len(labeled),6),"score_mean":round(statistics.mean(scores),6),"score_stddev":round(statistics.pstdev(scores),6)}
 alerts=[]
 if m["p95_latency_ms"]>SLO["p95_latency_ms"]: alerts.append("InferenceLatencySLOBreach")
 if m["availability"]<SLO["availability"]: alerts.append("InferenceAvailabilitySLOBreach")
 if m["quality"]<SLO["min_quality"]: alerts.append("PredictionQualityFloorBreach")
 if m["score_stddev"]<SLO["min_score_stddev"]: alerts.append("DegenerateScoreDistribution")
 return {"metrics":m,"alerts":alerts,"fallback_engaged":bool(alerts)}
def fixture():
 rng=random.Random(202); rows=[]
 for window in ("healthy","latency_breach","degenerate_quality_breach"):
  for i in range(240):
   failed=window!="healthy" and i<5
   latency=rng.uniform(18,55) if window!="latency_breach" else rng.uniform(90,180)
   score=rng.uniform(.15,.95) if window!="degenerate_quality_breach" else .5
   quality=.92 if window=="healthy" else .68 if window=="degenerate_quality_breach" else .88
   rows.append({"window":window,"request_id":f"{window}-{i}","latency_ms":round(latency,4),"success":int(not failed),"score":round(score,5),"correct":int(rng.random()<quality)})
 return rows
def main():
 rows=fixture(); data=ROOT/"data"; out=ROOT/"outputs"; data.mkdir(exist_ok=True); out.mkdir(exist_ok=True)
 with (data/"slo_events_fixture.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n"); w.writeheader(); w.writerows(rows)
 windows={name:evaluate([r for r in rows if r["window"]==name]) for name in ("healthy","latency_breach","degenerate_quality_breach")}
 month_minutes=30*24*60; budget=month_minutes*(1-SLO["availability"]); observed_failed=sum(not int(r["success"]) for r in rows); observed_downtime=observed_failed/len(rows)*15
 report={"data_source":"deterministic operational fixture","slo":SLO,"windows":windows,"error_budget":{"period_days":30,"allowed_unavailable_minutes":round(budget,3),"observed_equivalent_minutes":round(observed_downtime,3),"percent_consumed":round(observed_downtime/budget*100,4),"policy":"freeze risky releases at >=100%; investigate at >=50%"},"synthetic_breach_verified":all(windows[x]["alerts"] for x in ("latency_breach","degenerate_quality_breach"))}
 (out/"slo_evaluation.json").write_text(json.dumps(report,indent=2)+"\n")
 fig,ax=plt.subplots(figsize=(8,4));
 for name in ("healthy","degenerate_quality_breach"): ax.hist([float(r["score"]) for r in rows if r["window"]==name],bins=15,alpha=.55,label=name)
 ax.set_xlabel("Prediction score"); ax.set_ylabel("Count"); ax.set_title("Score-distribution monitoring"); ax.legend(); fig.tight_layout(); fig.savefig(out/"score_distribution.png",dpi=160); plt.close(fig)
 print(json.dumps(report,indent=2)); assert windows["healthy"]["alerts"]==[] and report["synthetic_breach_verified"]
if __name__=="__main__": main()
