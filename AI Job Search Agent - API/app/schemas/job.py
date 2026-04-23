from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.profile import SearchProfile


class JobPosting(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience_text: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    summary: str = ""
    description: str = ""
    apply_url: Optional[str] = None
    source_url: str
    match_score: float = 0.0
    match_reasons: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    profile: SearchProfile
    total_found: int
    jobs: List[JobPosting]