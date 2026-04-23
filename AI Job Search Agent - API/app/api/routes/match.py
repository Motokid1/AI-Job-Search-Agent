import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.job_match import SelectedJobInput
from app.services.job_detail_service import fetch_detailed_job
from app.services.job_fit_service import analyze_resume_against_job
from app.services.profile_service import extract_profile_from_resume, merge_resume_and_manual_profile

router = APIRouter(tags=["Job Match"])


@router.post("/jobs/detail")
async def get_job_detail(job_payload: str = Form(...)):
    try:
        payload = json.loads(job_payload)
        job = SelectedJobInput(**payload)
        detailed_job = fetch_detailed_job(job)
        return detailed_job.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Job detail fetch failed: {exc}")


@router.post("/match/job-resume")
async def match_resume_for_selected_job(
    file: UploadFile = File(...),
    job_payload: str = Form(...),
):
    try:
        payload = json.loads(job_payload)
        job = SelectedJobInput(**payload)

        file_bytes = await file.read()
        extracted = extract_profile_from_resume(file.filename, file_bytes)

        profile = merge_resume_and_manual_profile(
            extracted=extracted,
            package_min_lpa=None,
            package_max_lpa=None,
            companies=[job.company] if job.company else [],
            location_override=job.location,
            desired_role_override=job.title,
        )

        detailed_job = fetch_detailed_job(job)
        analysis = analyze_resume_against_job(profile=profile, detailed_job=detailed_job)

        return analysis.model_dump()

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Job-specific resume match failed: {exc}")