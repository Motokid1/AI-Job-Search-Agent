from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.profile import SearchProfile


class SelectedJobInput(BaseModel):
    title: str
    company: str
    source_url: str
    apply_url: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)


class DetailedJob(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience_text: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    tools_frameworks: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    summary: str = ""
    description: str = ""
    responsibilities: List[str] = Field(default_factory=list)
    apply_url: Optional[str] = None
    source_url: str


class JobFitSummary(BaseModel):
    overall_match_score: float
    skills_match_score: float
    ats_match_score: float
    experience_match_score: float
    project_relevance_score: float
    certification_match_score: float
    summary: str = ""


class JobFitGaps(BaseModel):
    missing_skills: List[str] = Field(default_factory=list)
    missing_tools_frameworks: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    missing_certifications: List[str] = Field(default_factory=list)
    experience_gaps: List[str] = Field(default_factory=list)
    project_alignment_issues: List[str] = Field(default_factory=list)


class JobResumeImprovements(BaseModel):
    summary_improvements: List[str] = Field(default_factory=list)
    project_bullet_improvements: List[str] = Field(default_factory=list)
    keyword_improvements: List[str] = Field(default_factory=list)
    skills_section_improvements: List[str] = Field(default_factory=list)


class JobResumeMatchResponse(BaseModel):
    profile: SearchProfile
    selected_job: DetailedJob
    job_fit_summary: JobFitSummary
    strengths: List[str] = Field(default_factory=list)
    gaps: JobFitGaps
    resume_improvements: JobResumeImprovements
    final_recommendation: str = ""