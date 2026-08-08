"""Concurrent local load test with overload fallback and breaking-point detection."""
import csv,json,math,random,statistics,threading,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent; CAPACITY=8; SLO_MS=100; TARGET_CONCURRENCY=8
def percentile(v,q):
 o=sorted(v); return o[min(len(o)-1,math.ceil(len(o)*q)-1)]
class Service:
 def __init__(self): self.slots=threading.BoundedSemaphore(CAPACITY)
 def predict(self,payload):
  start=time.perf_counter()
  if not self.slots.acquire(blocking=False): return {"latency_ms":(time.perf_counter()-start)*1000,"fallback":True,"quality":.82,"reason":"overload"}
  try:
   time.sleep(.004); score=sum(payload)/len(payload); return {"latency_ms":(time.perf_counter()-start)*1000,"fallback":False,"quality":.92,"score":score}
  finally: self.slots.release()
def run_level(concurrency,batches=30):
 service=Service(); rng=random.Random(404+concurrency); results=[]; start=time.perf_counter()
 with ThreadPoolExecutor(max_workers=concurrency) as pool:
  for _ in range(batches):
   barrier=threading.Barrier(concurrency)
   def call(): barrier.wait(); return service.predict([rng.random() for _ in range(12)])
   results.extend(f.result() for f in [pool.submit(call) for _ in range(concurrency)])
 elapsed=time.perf_counter()-start; fallbacks=sum(r["fallback"] for r in results); return {"concurrency":concurrency,"requests":len(results),"duration_s":round(elapsed,6),"achieved_qps":round(len(results)/elapsed,3),"p95_latency_ms":round(percentile([r["latency_ms"] for r in results],.95),4),"fallback_rate":round(fallbacks/len(results),6),"mean_quality":round(statistics.mean(r["quality"] for r in results),6),"slo_pass":percentile([r["latency_ms"] for r in results],.95)<=SLO_MS and fallbacks/len(results)<=.01}
def main():
 levels=[1,2,4,8,16,32]; results=[run_level(c) for c in levels]; breaking=next(x for x in results if not x["slo_pass"]); healthy=[x for x in results if x["slo_pass"]]; target=next(x for x in results if x["concurrency"]==TARGET_CONCURRENCY); report={"environment":"local measured load fixture","capacity_slots":CAPACITY,"target_concurrency":TARGET_CONCURRENCY,"slo":{"p95_latency_ms":SLO_MS,"max_fallback_rate":.01},"levels":results,"last_healthy":healthy[-1],"breaking_point":breaking,"concurrency_headroom_percent":round((breaking["concurrency"]-TARGET_CONCURRENCY)/TARGET_CONCURRENCY*100,2),"target_qps":target["achieved_qps"],"fallback_verified":breaking["fallback_rate"]>0}
 out=ROOT/"outputs"; out.mkdir(exist_ok=True); (out/"load_test_report.json").write_text(json.dumps(report,indent=2)+"\n")
 with (out/"load_test_results.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=results[0].keys(),lineterminator="\n"); w.writeheader(); w.writerows(results)
 fig,ax1=plt.subplots(figsize=(8,4)); ax1.plot(levels,[x["achieved_qps"] for x in results],marker="o",label="QPS"); ax1.set_xlabel("Concurrency"); ax1.set_ylabel("Achieved QPS"); ax2=ax1.twinx(); ax2.plot(levels,[x["fallback_rate"]*100 for x in results],color="red",marker="s",label="Fallback %"); ax2.set_ylabel("Fallback rate (%)"); ax1.axvline(breaking["concurrency"],linestyle="--",color="black"); fig.tight_layout(); fig.savefig(out/"load_curve.png",dpi=160); plt.close(fig)
 print(json.dumps(report,indent=2)); assert target["slo_pass"] and report["fallback_verified"]
if __name__=="__main__": main()
