import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.apply import ApplicationPreferenceInput
from app.schemas.job_match import SelectedJobInput
from app.services.auto_apply_service import generate_auto_apply_package
from app.services.job_detail_service import fetch_detailed_job
from app.services.profile_service import extract_profile_from_resume, merge_resume_and_manual_profile

router = APIRouter(tags=["Auto Apply Assistant"])


@router.post("/apply/prepare")
async def prepare_application_package(
    file: UploadFile = File(...),
    job_payload: str = Form(...),
    cover_letter_tone: str | None = Form(default="professional"),
    notice_period: str | None = Form(default=None),
    expected_salary: str | None = Form(default=None),
    current_location: str | None = Form(default=None),
    willing_to_relocate: str | None = Form(default=None),
    work_authorization: str | None = Form(default=None),
    portfolio_url: str | None = Form(default=None),
    github_url: str | None = Form(default=None),
    linkedin_url: str | None = Form(default=None),
):
    try:
        payload = json.loads(job_payload)
        selected_job_input = SelectedJobInput(**payload)

        file_bytes = await file.read()
        extracted = extract_profile_from_resume(file.filename, file_bytes)

        profile = merge_resume_and_manual_profile(
            extracted=extracted,
            package_min_lpa=None,
            package_max_lpa=None,
            companies=[selected_job_input.company] if selected_job_input.company else [],
            location_override=current_location or selected_job_input.location,
            desired_role_override=selected_job_input.title,
        )

        detailed_job = fetch_detailed_job(selected_job_input)

        preferences = ApplicationPreferenceInput(
            cover_letter_tone=cover_letter_tone,
            notice_period=notice_period,
            expected_salary=expected_salary,
            current_location=current_location,
            willing_to_relocate=willing_to_relocate,
            work_authorization=work_authorization,
            portfolio_url=portfolio_url,
            github_url=github_url,
            linkedin_url=linkedin_url,
        )

        result = generate_auto_apply_package(
            profile=profile,
            selected_job=detailed_job,
            preferences=preferences,
        )

        return result.model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Application package generation failed: {exc}",
        )