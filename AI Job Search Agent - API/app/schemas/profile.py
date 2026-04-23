from typing import List, Optional

from pydantic import BaseModel, Field


class ManualProfileInput(BaseModel):
    desired_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    years_experience: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    package_min_lpa: Optional[float] = None
    package_max_lpa: Optional[float] = None
    companies: List[str] = Field(default_factory=list)


class ResumeExtractedProfile(BaseModel):
    desired_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    years_experience: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    projects: List[str] = Field(default_factory=list)
    summary: str = ""
    raw_resume_text: str = ""


class SearchProfile(BaseModel):
    desired_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    years_experience: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    package_min_lpa: Optional[float] = None
    package_max_lpa: Optional[float] = None
    companies: List[str] = Field(default_factory=list)
    summary: str = ""
    raw_resume_text: Optional[str] = None

    def to_search_text(self) -> str:
        parts = []

        if self.desired_role:
            parts.append(f"Desired Role: {self.desired_role}")
        if self.skills:
            parts.append(f"Skills: {', '.join(self.skills)}")
        if self.years_experience is not None:
            parts.append(f"Experience: {self.years_experience} years")
        if self.certifications:
            parts.append(f"Certifications: {', '.join(self.certifications)}")
        if self.location:
            parts.append(f"Preferred Location: {self.location}")
        if self.package_min_lpa is not None or self.package_max_lpa is not None:
            parts.append(
                f"Expected Package: {self.package_min_lpa or ''} - {self.package_max_lpa or ''} LPA"
            )
        if self.companies:
            parts.append(f"Preferred Companies: {', '.join(self.companies)}")
        if self.summary:
            parts.append(f"Profile Summary: {self.summary}")

        return "\n".join(parts)