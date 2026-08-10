def test_api_full_partial_failure_and_validation(candidate):
 from src.api import create_app
 client=create_app().test_client()
 for payload in [{"candidate":candidate.model_dump(mode="json"),"k":5},{"candidate":{"candidate_id":"partial"}},{"candidate":{"candidate_id":"fail"},"force_model_failure":True}]:
  r=client.post("/api/v1/recommendations/cold-start",json=payload);assert r.status_code==200 and r.get_json()["recommendations"]
 assert client.post("/api/v1/recommendations/cold-start",json={"candidate":{"candidate_id":"x","verified_scores":{"python":2}}}).status_code==422
