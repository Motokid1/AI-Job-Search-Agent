from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.job_match import DetailedJob
from app.schemas.profile import SearchProfile


class ApplicationPreferenceInput(BaseModel):
    cover_letter_tone: Optional[str] = "professional"
    notice_period: Optional[str] = None
    expected_salary: Optional[str] = None
    current_location: Optional[str] = None
    willing_to_relocate: Optional[str] = None
    work_authorization: Optional[str] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class ApplicationAnswer(BaseModel):
    question: str
    answer: str


class AutoApplyLLMOutput(BaseModel):
    apply_readiness_score: float
    final_recommendation: str
    resume_improvement_notes: List[str] = Field(default_factory=list)
    cover_letter: str
    application_answers: List[ApplicationAnswer] = Field(default_factory=list)
    recruiter_message: str
    referral_message: str
    apply_checklist: List[str] = Field(default_factory=list)
    risk_warnings: List[str] = Field(default_factory=list)


class AutoApplyPackageResponse(BaseModel):
    profile: SearchProfile
    selected_job: DetailedJob
    apply_readiness_score: float
    final_recommendation: str
    resume_improvement_notes: List[str] = Field(default_factory=list)
    cover_letter: str
    application_answers: List[ApplicationAnswer] = Field(default_factory=list)
    recruiter_message: str
    referral_message: str
    apply_checklist: List[str] = Field(default_factory=list)
    risk_warnings: List[str] = Field(default_factory=list)
    apply_url: Optional[str] = None
    safety_note: str = (
        "This assistant prepares application material only. "
        "The user must review and submit the application manually."
    )