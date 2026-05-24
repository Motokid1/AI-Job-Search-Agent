from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AutoApplyStatus(str, Enum):
    created = "created"
    opening_browser = "opening_browser"
    form_detected = "form_detected"
    filling_form = "filling_form"
    waiting_for_approval = "waiting_for_approval"
    submitted = "submitted"
    cancelled = "cancelled"
    blocked = "blocked"
    failed = "failed"


class AutoApplyCandidateInput(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    expected_salary: Optional[str] = None
    notice_period: Optional[str] = None
    willing_to_relocate: Optional[str] = None
    work_authorization: Optional[str] = None
    cover_letter: Optional[str] = None


class AutoApplySessionResponse(BaseModel):
    session_id: str
    status: AutoApplyStatus
    current_step: str
    message: str
    browser_url: Optional[str] = None
    requires_user_action: bool = False
    detected_fields: List[Dict[str, Any]] = Field(default_factory=list)


class AutoApplyResumeRequest(BaseModel):
    decision: str