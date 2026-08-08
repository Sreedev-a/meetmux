"""Load, failure-injection, observability, and reliability sign-off."""
import hashlib,json,math,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import matplotlib.pyplot as plt
from service import create_app,predict,reset_metrics,snapshot
ROOT=Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 reset_metrics(); query=[.9,.8,.7]; expected=predict(query)["results"][0]["job_id"]; reset_metrics(); start=time.perf_counter()
 with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(lambda _:predict(query),range(400)))
 duration=time.perf_counter()-start; metrics=snapshot(); quality=sum(r["results"][0]["job_id"]==expected for r in results)/len(results); injected=predict(query,True); client=create_app().test_client(); metrics_endpoint=client.get("/metrics").get_json()
 prior=ROOT.parent/"Phase3_SprintA_Task04_Horizontal_Scale_and_Load_Readiness/outputs/load_test_report.json"; headroom=json.loads(prior.read_text())
 evidence={"load":{"requests":len(results),"concurrency":8,"duration_s":round(duration,6),"qps":round(len(results)/duration,3),**{k:round(v,6) for k,v in metrics.items()},"quality":quality},"slos":{"p95_latency_ms_max":100,"availability_min":.995,"quality_min":.80,"fallback_rate_max":.01},"failure_injection":{"fallback":injected["fallback"],"reason":injected["reason"],"response_count":len(injected["results"])},"monitoring_endpoint":metrics_endpoint,"headroom":{"source":"Sprint A Task 4 executed report","sha256":sha(prior),"breaking_concurrency":headroom["breaking_point"]["concurrency"],"headroom_percent":headroom["concurrency_headroom_percent"]}}
 checks={"p95_slo":metrics["p95_latency_ms"]<=100,"availability_slo":metrics["availability"]>=.995,"quality_floor":quality>=.8,"fallback_rate":metrics["fallback_rate"]<=.01,"forced_failure_fallback":injected["fallback"],"headroom_at_least_50_percent":headroom["concurrency_headroom_percent"]>=50,"monitoring_live":metrics_endpoint["requests"]>0}; report={**evidence,"checks":checks,"decision":"SIGNED_OFF_LOCAL_SCALE_BASELINE" if all(checks.values()) else "BLOCKED","owner":"ML Reliability Owner","residual_risks":["Production traffic and infrastructure may differ from local fixture","Production observability deployment remains an external DevOps action"]}
 out=ROOT/"outputs"; out.mkdir(exist_ok=True); (out/"reliability_signoff.json").write_text(json.dumps(report,indent=2)+"\n")
 fig,ax=plt.subplots(figsize=(7,4)); ax.bar(["p95 latency","SLO"],[metrics["p95_latency_ms"],100],color=["#2e8b57","#808080"]); ax.set_ylabel("Milliseconds"); ax.set_title("Integrated service load sign-off"); fig.tight_layout(); fig.savefig(out/"integrated_load.png",dpi=160); plt.close(fig)
 print(json.dumps(report,indent=2)); assert all(checks.values())
if __name__=="__main__": main()
