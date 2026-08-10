"""Type-safe marketplace contracts suitable for a future FastAPI service."""

from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

NormalizedScore = Annotated[float, Field(ge=0.0, le=1.0)]
NonEmptyText = Annotated[str, Field(min_length=1)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class WorkMode(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"


class Education(StrictModel):
    qualification: NonEmptyText
    field_of_study: NonEmptyText | None = None
    institution: NonEmptyText | None = None
    graduation_year: int | None = Field(default=None, ge=1950, le=2100)


class StudentProfile(StrictModel):
    student_id: NonEmptyText
    name: NonEmptyText
    verified_scores: dict[str, NormalizedScore]
    self_reported_skills: list[NonEmptyText] = Field(default_factory=list)
    years_experience: float = Field(default=0.0, ge=0.0, le=60.0)
    education: Education | None = None
    available_from: str | None = None
    preferred_locations: list[NonEmptyText] = Field(default_factory=list)
    accepted_work_modes: set[WorkMode] = Field(default_factory=set)
    desired_employment_types: set[EmploymentType] = Field(default_factory=set)

    @field_validator("verified_scores")
    @classmethod
    def validate_skill_identifiers(cls, scores: dict[str, float]) -> dict[str, float]:
        if not scores:
            raise ValueError("at least one verified score is required")
        if any(not key.strip() for key in scores):
            raise ValueError("skill identifiers cannot be empty")
        return scores


class JobProfile(StrictModel):
    job_id: NonEmptyText
    company_id: NonEmptyText
    title: NonEmptyText
    description: str = ""
    required_skills: dict[str, NormalizedScore]
    preferred_skills: dict[str, NormalizedScore] = Field(default_factory=dict)
    minimum_years_experience: float = Field(default=0.0, ge=0.0, le=60.0)
    location: NonEmptyText | None = None
    work_mode: WorkMode | None = None
    employment_type: EmploymentType | None = None

    @field_validator("required_skills", "preferred_skills")
    @classmethod
    def validate_skill_identifiers(cls, scores: dict[str, float]) -> dict[str, float]:
        if any(not key.strip() for key in scores):
            raise ValueError("skill identifiers cannot be empty")
        return scores

    @model_validator(mode="after")
    def validate_skill_groups(self) -> "JobProfile":
        from .feature_space import normalize_skill_name

        required = [normalize_skill_name(skill) for skill in self.required_skills]
        preferred = [normalize_skill_name(skill) for skill in self.preferred_skills]
        if len(required) != len(set(required)) or len(preferred) != len(set(preferred)):
            raise ValueError("duplicate skills after normalization")
        overlap = set(required) & set(preferred)
        if overlap:
            raise ValueError(f"skills cannot be required and preferred: {sorted(overlap)}")
        return self


class MatchRequest(StrictModel):
    student: StudentProfile
    job: JobProfile
    matching_version: str = "feature-space-v1"


class SkillBreakdown(StrictModel):
    student_score: NormalizedScore
    job_threshold: NormalizedScore
    required: bool
    meets_threshold: bool
    gap: float = Field(ge=0.0, le=1.0)


class MatchResponse(StrictModel):
    student_id: NonEmptyText
    job_id: NonEmptyText
    match_score: NormalizedScore
    eligible: bool
    matched_skills: list[str]
    skill_gaps: list[str]
    feature_breakdown: dict[str, SkillBreakdown]
    model_version: str = "matching-foundation-v1"


class ErrorDetail(StrictModel):
    code: NonEmptyText
    message: NonEmptyText
    details: list[dict[str, Any]] = Field(default_factory=list)


class ErrorResponse(StrictModel):
    error: ErrorDetail
