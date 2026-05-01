from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.config import get_settings
from app.core.prompts import PROFILE_EXTRACTION_PROMPT
from app.schemas.profile import ManualProfileInput, ResumeExtractedProfile, SearchProfile
from app.services.llm_service import get_llm
from app.utils.files import extract_text_from_resume
from app.utils.text import clean_text, normalize_list, safe_json_loads, truncate_text


def extract_profile_from_resume(filename: str, file_bytes: bytes) -> ResumeExtractedProfile:
    settings = get_settings()

    raw_text = extract_text_from_resume(filename, file_bytes)
    cleaned_text = truncate_text(clean_text(raw_text), max_chars=settings.max_content_chars)

    prompt = PromptTemplate.from_template(PROFILE_EXTRACTION_PROMPT)
    chain = prompt | get_llm() | StrOutputParser()
    response_text = chain.invoke({"resume_text": cleaned_text})

    data = safe_json_loads(response_text)

    return ResumeExtractedProfile(
        desired_role=data.get("desired_role"),
        skills=normalize_list(data.get("skills", [])),
        years_experience=data.get("years_experience"),
        certifications=normalize_list(data.get("certifications", [])),
        location=data.get("location"),
        projects=normalize_list(data.get("projects", [])),
        summary=data.get("summary", ""),
        raw_resume_text=cleaned_text,
    )


def merge_resume_and_manual_profile(
    extracted: ResumeExtractedProfile,
    package_min_lpa: float | None = None,
    package_max_lpa: float | None = None,
    companies: list[str] | None = None,
    location_override: str | None = None,
    desired_role_override: str | None = None,
) -> SearchProfile:
    return SearchProfile(
        desired_role=desired_role_override or extracted.desired_role,
        skills=extracted.skills,
        years_experience=extracted.years_experience,
        certifications=extracted.certifications,
        location=location_override or extracted.location,
        package_min_lpa=package_min_lpa,
        package_max_lpa=package_max_lpa,
        companies=companies or [],
        summary=extracted.summary,
        raw_resume_text=extracted.raw_resume_text,
    )


def build_search_profile_from_manual(manual: ManualProfileInput) -> SearchProfile:
    return SearchProfile(
        desired_role=manual.desired_role,
        skills=normalize_list(manual.skills),
        years_experience=manual.years_experience,
        certifications=normalize_list(manual.certifications),
        location=manual.location,
        package_min_lpa=manual.package_min_lpa,
        package_max_lpa=manual.package_max_lpa,
        companies=normalize_list(manual.companies),
        summary="",
        raw_resume_text=None,
    )