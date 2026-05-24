import json
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.auto_apply_runtime import (
    AutoApplyCandidateInput,
    AutoApplyResumeRequest,
    AutoApplySessionResponse,
    AutoApplyStatus,
)
from app.services.auto_apply_session_store import create_session, get_session, update_session
from app.services.playwright_auto_apply_service import PlaywrightAutoApplySession

router = APIRouter(tags=["Human Approved Auto Apply"])

UPLOAD_DIR = Path("uploads/auto_apply")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _session_response(session_id: str) -> AutoApplySessionResponse:
    session = get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Auto apply session not found.")

    return AutoApplySessionResponse(
        session_id=session_id,
        status=session.get("status", AutoApplyStatus.created),
        current_step=session.get("current_step", "created"),
        message=session.get("message", ""),
        browser_url=session.get("browser_url"),
        requires_user_action=session.get("requires_user_action", False),
        detected_fields=session.get("detected_fields", []),
    )


@router.post("/auto-apply/start")
async def start_auto_apply(
    file: UploadFile = File(...),
    job_payload: str = Form(...),
    candidate_payload: str = Form(...),
):
    session_id = str(uuid4())

    try:
        job = json.loads(job_payload)
        candidate_data = json.loads(candidate_payload)
        candidate = AutoApplyCandidateInput(**candidate_data)

        job_url = job.get("apply_url") or job.get("source_url")
        if not job_url:
            raise HTTPException(status_code=400, detail="Job apply URL is required.")

        resume_path = UPLOAD_DIR / f"{session_id}_{file.filename}"
        file_bytes = await file.read()
        resume_path.write_bytes(file_bytes)

        browser = PlaywrightAutoApplySession(session_id=session_id)

        create_session(
            session_id,
            {
                "status": AutoApplyStatus.created,
                "current_step": "created",
                "message": "Auto apply session created.",
                "job": job,
                "job_url": job_url,
                "candidate": candidate.model_dump(),
                "resume_path": str(resume_path),
                "browser": browser,
                "requires_user_action": False,
                "detected_fields": [],
                "browser_url": None,
                "filled_fields": [],
                "resume_uploaded": False,
            },
        )

        update_session(
            session_id,
            {
                "status": AutoApplyStatus.opening_browser,
                "current_step": "open_browser",
                "message": "Opening application page.",
            },
        )

        browser_url = await browser.open(job_url)

        blocker = await browser.detect_blockers()
        if blocker:
            update_session(
                session_id,
                {
                    "status": AutoApplyStatus.blocked,
                    "current_step": "blocked",
                    "message": blocker,
                    "browser_url": browser_url,
                    "requires_user_action": True,
                },
            )
            return _session_response(session_id).model_dump()

        fields = await browser.inspect_fields()

        update_session(
            session_id,
            {
                "status": AutoApplyStatus.form_detected,
                "current_step": "inspect_form",
                "message": f"Detected {len(fields)} form fields.",
                "browser_url": browser_url,
                "detected_fields": fields,
            },
        )

        filled_fields = await browser.fill_fields(candidate.model_dump())
        resume_uploaded = await browser.upload_resume(str(resume_path))

        update_session(
            session_id,
            {
                "status": AutoApplyStatus.waiting_for_approval,
                "current_step": "human_review",
                "message": (
                    f"Filled {len(filled_fields)} field(s). "
                    f"Resume uploaded: {resume_uploaded}. "
                    "Please review the browser before submission."
                ),
                "browser_url": browser_url,
                "filled_fields": filled_fields,
                "resume_uploaded": resume_uploaded,
                "requires_user_action": True,
            },
        )

        return _session_response(session_id).model_dump()

    except HTTPException:
        raise

    except Exception as exc:
        update_session(
            session_id,
            {
                "status": AutoApplyStatus.failed,
                "current_step": "failed",
                "message": f"Auto apply failed: {exc}",
                "requires_user_action": True,
            },
        )
        return _session_response(session_id).model_dump()


@router.get("/auto-apply/session/{session_id}")
def get_auto_apply_session(session_id: str):
    return _session_response(session_id).model_dump()


@router.post("/auto-apply/session/{session_id}/resume")
async def resume_auto_apply_session(session_id: str, payload: AutoApplyResumeRequest):
    session = get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Auto apply session not found.")

    try:
        browser = session.get("browser")

        if not browser:
            update_session(
                session_id,
                {
                    "status": AutoApplyStatus.failed,
                    "current_step": "browser_missing",
                    "message": "Browser session is missing. Please start a new auto apply session.",
                    "requires_user_action": True,
                },
            )
            return _session_response(session_id).model_dump()

        if payload.decision == "submit":
            submitted = await browser.submit_application()

            update_session(
                session_id,
                {
                    "status": AutoApplyStatus.submitted if submitted else AutoApplyStatus.failed,
                    "current_step": "submitted" if submitted else "submit_failed",
                    "message": (
                        "Application submitted successfully."
                        if submitted
                        else "Could not find or click submit button. Please continue manually."
                    ),
                    "browser_url": session.get("browser_url"),
                    "requires_user_action": not submitted,
                },
            )

        elif payload.decision == "cancel":
            await browser.close()

            update_session(
                session_id,
                {
                    "status": AutoApplyStatus.cancelled,
                    "current_step": "cancelled",
                    "message": "Auto apply session cancelled.",
                    "browser_url": session.get("browser_url"),
                    "requires_user_action": False,
                },
            )

        else:
            update_session(
                session_id,
                {
                    "status": AutoApplyStatus.waiting_for_approval,
                    "current_step": "manual_review",
                    "message": "Browser remains open for manual review.",
                    "browser_url": session.get("browser_url"),
                    "requires_user_action": True,
                },
            )

        return _session_response(session_id).model_dump()

    except Exception as exc:
        update_session(
            session_id,
            {
                "status": AutoApplyStatus.failed,
                "current_step": "failed",
                "message": f"Auto apply resume failed: {exc}",
                "browser_url": session.get("browser_url"),
                "requires_user_action": True,
            },
        )
        return _session_response(session_id).model_dump()


@router.post("/auto-apply/session/{session_id}/cancel")
async def cancel_auto_apply_session(session_id: str):
    session = get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Auto apply session not found.")

    try:
        browser = session.get("browser")

        if browser:
            await browser.close()

        update_session(
            session_id,
            {
                "status": AutoApplyStatus.cancelled,
                "current_step": "cancelled",
                "message": "Auto apply session cancelled.",
                "browser_url": session.get("browser_url"),
                "requires_user_action": False,
            },
        )

        return _session_response(session_id).model_dump()

    except Exception as exc:
        update_session(
            session_id,
            {
                "status": AutoApplyStatus.failed,
                "current_step": "cancel_failed",
                "message": f"Cancel failed: {exc}",
                "browser_url": session.get("browser_url"),
                "requires_user_action": True,
            },
        )
        return _session_response(session_id).model_dump()