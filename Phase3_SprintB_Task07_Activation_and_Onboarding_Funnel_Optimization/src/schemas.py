from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator

Score = float

class StrictModel(BaseModel): model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
class Experience(str,Enum): ENTRY="entry"; MID="mid"; SENIOR="senior"
class Source(str,Enum): PERSONALIZED="personalized_cold_start"; EXPLORATION="exploration"; POPULAR="popular_fallback"; RECENT="recent_fallback"
class CandidateProfile(StrictModel):
 candidate_id:str=Field(min_length=1); verified_scores:dict[str,float]=Field(default_factory=dict); preferred_roles:list[str]=Field(default_factory=list); preferred_locations:list[str]=Field(default_factory=list); experience_level:Experience=Experience.ENTRY; employment_types:list[str]=Field(default_factory=list); interaction_count:int=Field(default=0,ge=0)
 @field_validator("verified_scores")
 @classmethod
 def scores(cls,v):
  if any(not k.strip() or not 0<=x<=1 for k,x in v.items()): raise ValueError("skills must be non-empty and scores in [0,1]")
  return v
class Job(StrictModel):
 job_id:str=Field(min_length=1); title:str=Field(min_length=1); company_id:str; required_skills:dict[str,float]=Field(default_factory=dict); role_family:str; location:str; remote:bool=False; experience_level:Experience=Experience.ENTRY; employment_type:str="full_time"; active:bool=True; expires_on:date; popularity:float=Field(ge=0,le=1); quality:float=Field(ge=0,le=1); posted_days_ago:int=Field(ge=0)
class Recommendation(StrictModel):
 job_id:str; position:int=Field(ge=1); score:float=Field(ge=0,le=1); source:Source; exploration:bool; reason:str=Field(min_length=1); matched_skills:list[str]; skill_gaps:list[str]; impression_id:str|None=None
class ColdStartRequest(StrictModel):
 candidate:CandidateProfile; k:int=Field(default=5,ge=1,le=20); exploration_fraction:float=Field(default=.2,ge=0,le=.5); force_model_failure:bool=False
class ColdStartResponse(StrictModel):
 candidate_id:str; user_state:str="cold_start"; ranking_id:str; model_name:str; model_version:str; fallback_used:bool; fallback_tier:int|None=None; reason:str|None=None; recommendations:list[Recommendation]
