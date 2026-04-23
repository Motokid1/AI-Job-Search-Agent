from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from app.schemas.profile import ManualProfileInput
from app.services.job_search_service import search_jobs_for_profile
from app.services.profile_service import (
    build_search_profile_from_manual,
    extract_profile_from_resume,
    merge_resume_and_manual_profile,
)

router = APIRouter(tags=["Jobs"])


@router.post("/jobs/search/manual")
async def search_jobs_manual(payload: ManualProfileInput):
    try:
        profile = build_search_profile_from_manual(payload)
        response = search_jobs_for_profile(profile)
        return response.model_dump()
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Job search failed: {exc}")


@router.post("/jobs/search/resume")
async def search_jobs_resume(
    file: UploadFile = File(...),
    package_min_lpa: float | None = Form(default=None),
    package_max_lpa: float | None = Form(default=None),
    location: str | None = Form(default=None),
    desired_role: str | None = Form(default=None),
    companies: str | None = Form(default=None),
):
    try:
        file_bytes = await file.read()
        extracted = extract_profile_from_resume(file.filename, file_bytes)

        company_list = [c.strip() for c in (companies or "").split(",") if c.strip()]

        profile = merge_resume_and_manual_profile(
            extracted=extracted,
            package_min_lpa=package_min_lpa,
            package_max_lpa=package_max_lpa,
            companies=company_list,
            location_override=location,
            desired_role_override=desired_role,
        )

        response = search_jobs_for_profile(profile)
        return response.model_dump()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Job search failed due to external API/network issue: {exc}"
        )