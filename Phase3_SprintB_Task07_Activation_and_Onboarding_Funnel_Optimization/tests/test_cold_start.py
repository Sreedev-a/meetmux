from datetime import date
from src.cold_start import recommend,score_job
from src.schemas import CandidateProfile
def test_zero_history_and_rich_profile(candidate,inventory):
 r=recommend(candidate,inventory,5,.2,today=date(2026,8,10));assert candidate.interaction_count==0 and len(r.recommendations)==5 and all(x.reason for x in r.recommendations)
def test_partial_and_minimal_profiles(inventory):
 for c in [CandidateProfile(candidate_id="p",verified_scores={"python":.8}),CandidateProfile(candidate_id="m")]:assert recommend(c,inventory,5,today=date(2026,8,10)).recommendations
def test_stronger_skill_match_scores_higher(candidate,inventory):assert score_job(candidate,inventory[0])[0]>score_job(CandidateProfile(candidate_id="x"),inventory[0])[0]
def test_deterministic_order(candidate,inventory):
 a=recommend(candidate,inventory,5,.2,today=date(2026,8,10));b=recommend(candidate,inventory,5,.2,today=date(2026,8,10));assert [x.job_id for x in a.recommendations]==[x.job_id for x in b.recommendations]
def test_no_history_used(candidate,inventory):
 before=score_job(candidate,inventory[0]);candidate.interaction_count=99;assert score_job(candidate,inventory[0])==before
