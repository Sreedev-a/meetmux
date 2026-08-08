"""Marketplace entities and the v1 matching API contract."""
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

Score = Annotated[float, Field(ge=0, le=100)]


class WorkMode(str, Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"


class Student(BaseModel):
    student_id: str = Field(pattern=r"^stu_[A-Za-z0-9]+$")
    verified_skills: dict[str, Score]
    years_experience: float = Field(ge=0, le=50)
    preferred_locations: list[str] = Field(min_length=1)
    work_modes: set[WorkMode]
    expected_salary_lpa: float = Field(gt=0)


class Job(BaseModel):
    job_id: str = Field(pattern=r"^job_[A-Za-z0-9]+$")
    company_id: str = Field(pattern=r"^co_[A-Za-z0-9]+$")
    required_skills: dict[str, Score]
    optional_skills: dict[str, Score] = {}
    minimum_experience: float = Field(ge=0)
    locations: list[str] = Field(min_length=1)
    work_mode: WorkMode
    salary_lpa: float = Field(gt=0)

    @model_validator(mode="after")
    def unique_skill_groups(self):
        if set(self.required_skills) & set(self.optional_skills):
            raise ValueError("a skill cannot be both required and optional")
        return self


class MatchRequest(BaseModel):
    request_id: str
    student: Student
    jobs: list[Job] = Field(min_length=1, max_length=100)
    limit: int = Field(default=10, ge=1, le=50)


class FeatureContribution(BaseModel):
    feature: str
    value: float
    weight: float


class MatchResult(BaseModel):
    job_id: str
    score: float = Field(ge=0, le=1)
    eligible: bool
    contributions: list[FeatureContribution]


class MatchResponse(BaseModel):
    request_id: str
    feature_space_version: str = "1.0.0"
    results: list[MatchResult]
