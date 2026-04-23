from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.profile_service import extract_profile_from_resume

router = APIRouter(tags=["Resume"])


@router.post("/resume/extract")
async def extract_resume_profile(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        profile = extract_profile_from_resume(file.filename, file_bytes)
        return profile.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Resume extraction failed: {exc}")