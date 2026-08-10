import json
from flask import Flask,jsonify,request
from pydantic import ValidationError
from .cold_start import recommend
from .demo_data import jobs
from .schemas import ColdStartRequest
def create_app(inventory=None):
 app=Flask(__name__); inventory=inventory or jobs()
 @app.post("/api/v1/recommendations/cold-start")
 def endpoint():
  try:
   payload=ColdStartRequest.model_validate(request.get_json(silent=True) or {})
   return jsonify(recommend(payload.candidate,inventory,payload.k,payload.exploration_fraction,payload.force_model_failure).model_dump(mode="json"))
  except ValidationError as exc:return jsonify(error="validation_error",details=json.loads(exc.json(include_url=False))),422
 return app
