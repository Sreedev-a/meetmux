import json
from pathlib import Path
from app import create_app
p={"request_id":"demo","student":{"skills":{"python":85,"sql":75},"experience":2,"locations":["Bengaluru"],"modes":["hybrid","remote"]},"limit":3}; r=create_app().test_client().post("/v1/recommendations/jobs",json=p); out=Path(__file__).parent/"outputs"; out.mkdir(exist_ok=True); (out/"demo_response.json").write_text(json.dumps(r.get_json(),indent=2)+"\n"); print(r.get_json())
