from datetime import date
from pathlib import Path
from src.cold_start import recommend
from src.instrumentation import log_response
def test_task6_instrumentation(candidate,inventory,tmp_path):
 r=recommend(candidate,inventory,4,today=date(2026,8,10));events=log_response(r,candidate.candidate_id,Path(__file__).resolve().parents[2],tmp_path/"events.jsonl")
 assert len(events)==4 and [e.rank_position for e in events]==[1,2,3,4] and all(e.model_version=="cold-start-v1" for e in events)
def test_failure_order_valid(candidate,inventory):
 r=recommend(candidate,inventory,5,force_failure=True,today=date(2026,8,10));assert [x.position for x in r.recommendations]==list(range(1,6))
