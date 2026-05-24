from fastapi import APIRouter, HTTPException, Query

from app.schemas.tracker import ApplicationCreate, ApplicationUpdate
from app.services.tracker_service import (
    create_application,
    delete_application,
    list_applications,
    update_application,
)

router = APIRouter(tags=["Application Tracker"])


@router.post("/tracker/applications")
def create_tracker_application(payload: ApplicationCreate):
    try:
        return create_application(payload).model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save application: {exc}")


@router.get("/tracker/applications")
def get_tracker_applications(
    status: str | None = Query(default=None),
    sort_by: str = Query(default="updated_at"),
    sort_order: str = Query(default="desc"),
):
    try:
        return list_applications(
            status=status,
            sort_by=sort_by,
            sort_order=sort_order,
        ).model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load tracker: {exc}")


@router.put("/tracker/applications/{application_id}")
def update_tracker_application(application_id: str, payload: ApplicationUpdate):
    try:
        return update_application(application_id, payload).model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to update application: {exc}")


@router.delete("/tracker/applications/{application_id}")
def delete_tracker_application(application_id: str):
    try:
        delete_application(application_id)
        return {"message": "Application deleted successfully"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to delete application: {exc}")