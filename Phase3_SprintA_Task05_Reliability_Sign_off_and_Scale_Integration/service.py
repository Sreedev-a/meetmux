"""Integrated, monitored recommendation service with explicit fallback."""
from __future__ import annotations
import math,threading,time
from flask import Flask,jsonify,request

JOBS=[("j1",[.9,.8,.7]),("j2",[.7,.8,.9]),("j3",[.5,.6,.7]),("j4",[.8,.7,.6])]
PREPARED=[(jid,v,math.sqrt(sum(x*x for x in v))) for jid,v in JOBS]
LOCK=threading.Lock(); METRICS={"requests":0,"success":0,"fallback":0,"latency_ms":[]}; SLOTS=threading.BoundedSemaphore(8)
def rank(query):
 qn=math.sqrt(sum(x*x for x in query)); return sorted([{"job_id":jid,"score":round(sum(a*b for a,b in zip(query,v))/(qn*n),6)} for jid,v,n in PREPARED],key=lambda x:(-x["score"],x["job_id"]))
def predict(query,force_failure=False):
 start=time.perf_counter(); fallback=False
 try:
  if force_failure: raise RuntimeError("injected_model_failure")
  if not SLOTS.acquire(blocking=False): raise RuntimeError("overload")
  try: time.sleep(.001); results=rank(query)
  finally: SLOTS.release()
 except Exception as exc: fallback=True; results=[{"job_id":jid,"score":None} for jid,_,_ in PREPARED[:3]]; reason=str(exc)
 latency=(time.perf_counter()-start)*1000
 with LOCK: METRICS["requests"]+=1; METRICS["success"]+=int(not fallback); METRICS["fallback"]+=int(fallback); METRICS["latency_ms"].append(latency)
 response={"results":results,"model_version":"2.0.0","fallback":fallback,"latency_ms":round(latency,6)}
 if fallback: response["reason"]=reason
 return response
def reset_metrics():
 with LOCK: METRICS.update({"requests":0,"success":0,"fallback":0,"latency_ms":[]})
def snapshot():
 with LOCK:
  lat=sorted(METRICS["latency_ms"]); n=METRICS["requests"]; return {"requests":n,"availability":METRICS["success"]/n if n else 1,"fallback_rate":METRICS["fallback"]/n if n else 0,"p95_latency_ms":lat[max(0,math.ceil(.95*len(lat))-1)] if lat else 0}
def create_app():
 app=Flask(__name__)
 @app.post("/predict")
 def endpoint():
  p=request.get_json(silent=True) or {}; q=p.get("features")
  if not isinstance(q,list) or len(q)!=3 or not all(isinstance(x,(int,float)) and x>=0 for x in q): return jsonify(error="features_must_be_three_nonnegative_numbers"),422
  return jsonify(predict(q,bool(p.get("force_failure"))))
 @app.get("/metrics")
 def metrics(): return jsonify(snapshot())
 @app.get("/health")
 def health(): return jsonify(status="ok",model_version="2.0.0")
 return app
app=create_app()
if __name__=="__main__": app.run(port=8025)
