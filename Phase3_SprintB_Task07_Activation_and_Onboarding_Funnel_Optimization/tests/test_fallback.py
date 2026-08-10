from datetime import date
from src.cold_start import recommend
from src.schemas import CandidateProfile
def test_force_failure_nonempty_metadata(inventory):
 r=recommend(CandidateProfile(candidate_id="x"),inventory,5,force_failure=True,today=date(2026,8,10));assert len(r.recommendations)==5 and r.fallback_used and r.fallback_tier==1 and r.model_version=="cold-start-fallback-v1"
def test_empty_market_safe(candidate):
 r=recommend(candidate,[],5,today=date(2026,8,10));assert r.recommendations==[] and r.reason=="no_eligible_jobs"
