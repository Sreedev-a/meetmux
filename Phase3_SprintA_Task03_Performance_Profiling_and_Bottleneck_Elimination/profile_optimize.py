"""Profile baseline matching and verify an equivalent optimized path."""
import cProfile,io,json,math,pstats,random,statistics,time
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent; SEED=303
def catalog(n=500):
 rng=random.Random(SEED); return [{"id":f"j{i:04d}","skills":[rng.uniform(20,100) for _ in range(12)],"active":i%17!=0} for i in range(n)]
def baseline(query,jobs):
 rows=[]
 for job in jobs:
  if not job["active"]: continue
  qnorm=math.sqrt(sum(x*x for x in query)); jnorm=math.sqrt(sum(x*x for x in job["skills"])); dot=sum(a*b for a,b in zip(query,job["skills"])); rows.append((dot/(qnorm*jnorm),job["id"]))
 return sorted(rows,key=lambda x:(-x[0],x[1]))[:10]
def prepare(jobs):
 return [(j["id"],j["skills"],math.sqrt(sum(x*x for x in j["skills"]))) for j in jobs if j["active"]]
def optimized(query,prepared):
 qnorm=math.sqrt(sum(x*x for x in query)); rows=[(sum(a*b for a,b in zip(query,skills))/(qnorm*norm),jid) for jid,skills,norm in prepared]; return sorted(rows,key=lambda x:(-x[0],x[1]))[:10]
def safe_predict(query,prepared,available=True):
 return {"results":optimized(query,prepared),"fallback":False} if available else {"results":[(0.0,jid) for jid,_,_ in prepared[:10]],"fallback":True,"reason":"model_unavailable"}
def benchmark(fn,iterations=250):
 times=[]
 for _ in range(iterations):
  start=time.perf_counter(); fn(); times.append((time.perf_counter()-start)*1000)
 ordered=sorted(times); return {"iterations":iterations,"mean_ms":round(statistics.mean(times),6),"median_ms":round(statistics.median(times),6),"p95_ms":round(ordered[math.ceil(.95*len(ordered))-1],6),"max_ms":round(max(times),6)}
def main():
 jobs=catalog(); query=[35+i*4 for i in range(12)]; prepared=prepare(jobs); out=ROOT/"outputs"; out.mkdir(exist_ok=True)
 profiler=cProfile.Profile(); profiler.enable(); [baseline(query,jobs) for _ in range(20)]; profiler.disable(); stream=io.StringIO(); pstats.Stats(profiler,stream=stream).sort_stats("cumtime").print_stats(15); (out/"baseline_profile.txt").write_text(stream.getvalue().rstrip()+"\n")
 before=benchmark(lambda:baseline(query,jobs)); after=benchmark(lambda:optimized(query,prepared)); b=baseline(query,jobs); a=optimized(query,prepared); exact=all(x[1]==y[1] and abs(x[0]-y[0])<1e-12 for x,y in zip(b,a)); fallback=safe_predict(query,prepared,False)
 report={"fixture":{"jobs":len(jobs),"features":len(query),"seed":SEED},"before":before,"after":after,"speedup":round(before["mean_ms"]/after["mean_ms"],4),"p95_reduction_percent":round((before["p95_ms"]-after["p95_ms"])/before["p95_ms"]*100,4),"cpu_seconds_per_million_requests":{"before":round(before["mean_ms"]*1000,3),"after":round(after["mean_ms"]*1000,3)},"quality":{"top10_exact_match":exact,"max_score_delta":max(abs(x[0]-y[0]) for x,y in zip(b,a))},"latency_slo_ms":100,"optimized_meets_slo":after["p95_ms"]<=100,"failure_path":fallback}
 (out/"before_after.json").write_text(json.dumps(report,indent=2)+"\n")
 fig,ax=plt.subplots(figsize=(7,4)); ax.bar(["baseline","optimized"],[before["p95_ms"],after["p95_ms"]],color=["#b22222","#2e8b57"]); ax.set_ylabel("p95 latency (ms)"); ax.set_title("Inference latency before/after"); fig.tight_layout(); fig.savefig(out/"latency_comparison.png",dpi=160); plt.close(fig)
 print(json.dumps(report,indent=2)); assert exact and report["optimized_meets_slo"] and fallback["fallback"] and report["speedup"]>1
if __name__=="__main__": main()
