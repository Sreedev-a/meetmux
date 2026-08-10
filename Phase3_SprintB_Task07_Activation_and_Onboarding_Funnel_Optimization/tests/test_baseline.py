from datetime import date
from src.baseline import rank_baseline
def test_baseline_valid_count(candidate,inventory):
 rows=rank_baseline(candidate,inventory,5,date(2026,8,10));assert len(rows)==5 and all(x.active for x in rows)
def test_expired_excluded(candidate,inventory):assert "job_expired" not in [x.job_id for x in rank_baseline(candidate,inventory,20,date(2026,8,10))]
