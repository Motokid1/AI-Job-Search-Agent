from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.profile import SearchProfile


class AnalysisInput(BaseModel):
    target_role: str
    package_min_lpa: Optional[float] = None
    package_max_lpa: Optional[float] = None
    companies: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    target_domain: Optional[str] = None


class MarketRequirement(BaseModel):
    role: str
    skills: List[str] = Field(default_factory=list)
    tools_frameworks: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    experience_expectations: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    summary: str = ""
    source_url: str


class LearningResource(BaseModel):
    title: str
    resource_type: str = "other"
    skills_covered: List[str] = Field(default_factory=list)
    summary: str = ""
    difficulty: str = "unknown"
    url: str


class FitAnalysis(BaseModel):
    resume_strength_score: float
    role_readiness_score: float
    package_readiness_score: float
    ats_score: float
    strengths: List[str] = Field(default_factory=list)
    overall_summary: str = ""


class GapReport(BaseModel):
    missing_skills: List[str] = Field(default_factory=list)
    missing_tools_frameworks: List[str] = Field(default_factory=list)
    missing_certifications: List[str] = Field(default_factory=list)
    weak_projects: List[str] = Field(default_factory=list)
    weak_keywords: List[str] = Field(default_factory=list)
    experience_gap: str = ""


class ResumeModifications(BaseModel):
    summary_suggestions: List[str] = Field(default_factory=list)
    project_rewrite_suggestions: List[str] = Field(default_factory=list)
    skills_section_improvements: List[str] = Field(default_factory=list)
    missing_sections: List[str] = Field(default_factory=list)
    ats_keyword_improvements: List[str] = Field(default_factory=list)


class CareerGrowthSuggestions(BaseModel):
    skills_to_learn_next: List[str] = Field(default_factory=list)
    certifications_to_consider: List[str] = Field(default_factory=list)
    projects_to_build: List[str] = Field(default_factory=list)
    interview_topics: List[str] = Field(default_factory=list)


class ResumeAnalysisResponse(BaseModel):
    profile: SearchProfile
    target_role: str
    package_min_lpa: Optional[float] = None
    package_max_lpa: Optional[float] = None
    location: Optional[str] = None
    companies: List[str] = Field(default_factory=list)
    target_domain: Optional[str] = None
    market_requirements: List[MarketRequirement] = Field(default_factory=list)
    learning_resources: List[LearningResource] = Field(default_factory=list)
    fit_analysis: FitAnalysis
    gap_report: GapReport
    resume_modifications: ResumeModifications
    career_growth_suggestions: CareerGrowthSuggestions
    final_recommendation: str = ""