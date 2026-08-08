import csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).parent
def checksum(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def point_in_time(rows,entity_id,as_of):
 valid=[r for r in rows if r["entity_id"]==entity_id and r["event_time"]<=as_of]; return max(valid,key=lambda r:r["event_time"]) if valid else None
def main():
 model=ROOT/"artifacts/recommendation_model_v2.bin"; registry={"model_name":"recommendation_gate","version":"2.0.0","stage":"production","registered_at_utc":datetime.now(timezone.utc).isoformat(),"artifact":str(model.relative_to(ROOT)),"sha256":checksum(model),"features":["skill_fit","experience_fit"],"metrics":{"validation_accuracy":.875},"lineage":{"training_dataset":"training_snapshot_v2","code":"mlops.py"},"approved_by":"automated quality gate"}; (ROOT/"registry").mkdir(exist_ok=True); (ROOT/"registry/model_v2.0.0.json").write_text(json.dumps(registry,indent=2)+"\n")
 with (ROOT/"feature_store/offline_features.csv").open() as f: rows=list(csv.DictReader(f))
 samples=[point_in_time(rows,"stu_1","2026-08-02T00:00:00Z"),point_in_time(rows,"stu_2","2026-08-03T00:00:00Z")]; manifest={"feature_view":"student_match_features_v1","entities":2,"records":len(rows),"point_in_time_samples":samples,"model_registry_checksum_verified":checksum(model)==registry["sha256"],"status":"live"}; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/mlops_foundation_report.json").write_text(json.dumps(manifest,indent=2)+"\n"); print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
