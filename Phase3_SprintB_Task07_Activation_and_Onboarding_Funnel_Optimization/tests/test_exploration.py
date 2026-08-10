from datetime import date
from src.cold_start import recommend
def test_exploration_nonzero_eligible_unique(candidate,inventory):
 r=recommend(candidate,inventory,5,.2,today=date(2026,8,10));assert sum(x.exploration for x in r.recommendations)==1 and len({x.job_id for x in r.recommendations})==5 and "job_expired" not in {x.job_id for x in r.recommendations}
def test_no_exploration_when_zero(candidate,inventory):assert not any(x.exploration for x in recommend(candidate,inventory,5,0,today=date(2026,8,10)).recommendations)
