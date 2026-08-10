"""Load and reuse Sprint B Task 6's exact event schema/logger."""
import importlib,sys,types
from pathlib import Path
def task6_components(repository_root:Path):
 name="task6_growth"; package=types.ModuleType(name); package.__path__=[str(repository_root/"Phase3_SprintB_Task06_Growth_Instrumentation_and_North_Star_Metrics/src")];sys.modules[name]=package
 store=importlib.import_module(name+".event_store");logger=importlib.import_module(name+".event_logger")
 return store.JsonlEventStore,logger.EventLogger
def log_response(response,candidate_id,repository_root,log_path):
 Store,Logger=task6_components(repository_root); store=Store(log_path); logger=Logger(store)
 for rec in response.recommendations:
  event=logger.log_impression(request_id="cold_start_demo_request",ranking_id=response.ranking_id,session_id="fresh_session_001",actor_id=candidate_id,item_id=rec.job_id,rank_position=rec.position,score=rec.score,model_name=response.model_name,model_version=response.model_version,context={"user_state":"cold_start","recommendation_source":rec.source.value,"exploration_item":rec.exploration,"fallback_used":response.fallback_used})
  rec.impression_id=event.impression_id
 return store.read_all()
