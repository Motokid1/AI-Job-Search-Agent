from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.analysis_service import generate_resume_analysis
from app.services.learning_resource_service import collect_learning_resources
from app.services.market_research_service import collect_market_requirements
from app.services.profile_service import extract_profile_from_resume, merge_resume_and_manual_profile

router = APIRouter(tags=["Analysis"])


@router.post("/analysis/resume")
async def analyze_resume(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    package_min_lpa: float | None = Form(default=None),
    package_max_lpa: float | None = Form(default=None),
    location: str | None = Form(default=None),
    companies: str | None = Form(default=None),
    target_domain: str | None = Form(default=None),
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
            desired_role_override=target_role,
        )

        market_requirements = collect_market_requirements(
            profile=profile,
            target_role=target_role,
            package_min_lpa=package_min_lpa,
            package_max_lpa=package_max_lpa,
            companies=company_list,
            location=location,
            target_domain=target_domain,
        )

        learning_resources = collect_learning_resources(
            target_role=target_role,
            target_domain=target_domain,
        )

        analysis = generate_resume_analysis(
            profile=profile,
            target_role=target_role,
            package_min_lpa=package_min_lpa,
            package_max_lpa=package_max_lpa,
            location=location,
            companies=company_list,
            target_domain=target_domain,
            market_requirements=market_requirements,
            learning_resources=learning_resources,
        )

        return analysis.model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {exc}",
        )