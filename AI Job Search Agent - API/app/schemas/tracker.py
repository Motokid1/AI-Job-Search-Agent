from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    saved = "Saved"
    applied = "Applied"
    screening = "Screening"
    interview = "Interview"
    final_round = "Final Round"
    offer = "Offer"
    rejected = "Rejected"


class ApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: str
    status: ApplicationStatus = ApplicationStatus.saved
    applied_date: Optional[date] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    recruiter_name: Optional[str] = None
    recruiter_contact: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_url: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    recruiter_name: Optional[str] = None
    recruiter_contact: Optional[str] = None


class ApplicationRecord(ApplicationCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class TrackerAnalytics(BaseModel):
    total_saved: int = 0
    total_applied: int = 0
    interviews_scheduled: int = 0
    offers_received: int = 0
    rejected_count: int = 0
    pending_followups: int = 0
    application_conversion_rate: float = 0.0


class TrackerResponse(BaseModel):
    applications: list[ApplicationRecord] = Field(default_factory=list)
    analytics: TrackerAnalytics