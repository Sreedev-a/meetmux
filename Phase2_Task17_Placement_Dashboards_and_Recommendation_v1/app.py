import json
from pathlib import Path
from flask import Flask,jsonify,request
ROOT=Path(__file__).parent; DATA=json.loads((ROOT/"data/catalog.json").read_text())
def recommend(student,limit=5):
 rows=[]
 for j in DATA["jobs"]:
  if not (j["active"] and j["company_verified"]): continue
  skill=sum(min(student.get("skills",{}).get(k,0)/v,1) for k,v in j["skills"].items())/len(j["skills"]); parts={"skill_fit":skill,"experience_fit":min(student.get("experience",0)/max(j["experience"],.1),1),"location_fit":float(j["location"] in student.get("locations",[])),"work_mode_fit":float(j["mode"] in student.get("modes",[]))}; score=.65*parts["skill_fit"]+.15*parts["experience_fit"]+.1*parts["location_fit"]+.1*parts["work_mode_fit"]; rows.append({"job_id":j["id"],"score":round(score,4),"contributions":parts,"model_version":"rec_v1.0.0"})
 if not student.get("skills"): rows=sorted(rows,key=lambda x:next(j["posted_at"] for j in DATA["jobs"] if j["id"]==x["job_id"]),reverse=True)
 else: rows=sorted(rows,key=lambda x:(-x["score"],x["job_id"]))
 return rows[:limit]
def create_app():
 app=Flask(__name__)
 @app.post("/v1/recommendations/jobs")
 def endpoint():
  p=request.get_json(silent=True) or {}; limit=p.get("limit",5)
  if not isinstance(limit,int) or not 1<=limit<=20: return jsonify(error="limit_must_be_1_to_20"),422
  return jsonify(request_id=p.get("request_id"),results=recommend(p.get("student",{}),limit))
 return app
app=create_app()
if __name__=="__main__": app.run(port=8017)
