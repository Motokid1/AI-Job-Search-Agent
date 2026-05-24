import json
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from app.schemas.tracker import (
    ApplicationCreate,
    ApplicationRecord,
    ApplicationStatus,
    ApplicationUpdate,
    TrackerAnalytics,
    TrackerResponse,
)

DATA_DIR = Path("data")
TRACKER_FILE = DATA_DIR / "application_tracker.json"


def _ensure_storage() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not TRACKER_FILE.exists():
        TRACKER_FILE.write_text("[]", encoding="utf-8")


def _load_records() -> list[dict]:
    _ensure_storage()
    return json.loads(TRACKER_FILE.read_text(encoding="utf-8"))


def _save_records(records: list[dict]) -> None:
    _ensure_storage()
    TRACKER_FILE.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")


def _parse_record(record: dict) -> ApplicationRecord:
    return ApplicationRecord(**record)


def create_application(payload: ApplicationCreate) -> ApplicationRecord:
    records = _load_records()
    now = datetime.utcnow()

    record = ApplicationRecord(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )

    records.append(record.model_dump())
    _save_records(records)

    return record


def list_applications(
    status: str | None = None,
    sort_by: str = "updated_at",
    sort_order: str = "desc",
) -> TrackerResponse:
    records = [_parse_record(item) for item in _load_records()]

    if status and status != "All":
        records = [item for item in records if item.status == status]

    reverse = sort_order.lower() == "desc"

    if sort_by in {"company", "role", "status", "applied_date", "follow_up_date", "created_at", "updated_at"}:
        records.sort(key=lambda item: str(getattr(item, sort_by) or ""), reverse=reverse)

    return TrackerResponse(
        applications=records,
        analytics=calculate_analytics(records),
    )


def update_application(application_id: str, payload: ApplicationUpdate) -> ApplicationRecord:
    records = _load_records()
    updated = None

    for index, record in enumerate(records):
        if record["id"] == application_id:
            current = _parse_record(record)
            update_data = payload.model_dump(exclude_unset=True)

            updated_record = current.model_copy(
                update={
                    **update_data,
                    "updated_at": datetime.utcnow(),
                }
            )

            records[index] = updated_record.model_dump()
            updated = updated_record
            break

    if not updated:
        raise ValueError("Application not found.")

    _save_records(records)
    return updated


def delete_application(application_id: str) -> None:
    records = _load_records()
    new_records = [record for record in records if record["id"] != application_id]

    if len(new_records) == len(records):
        raise ValueError("Application not found.")

    _save_records(new_records)


def calculate_analytics(records: list[ApplicationRecord]) -> TrackerAnalytics:
    today = date.today()

    total_saved = len(records)
    total_applied = len([r for r in records if r.status in {
        ApplicationStatus.applied,
        ApplicationStatus.screening,
        ApplicationStatus.interview,
        ApplicationStatus.final_round,
        ApplicationStatus.offer,
        ApplicationStatus.rejected,
    }])

    interviews = len([r for r in records if r.status in {
        ApplicationStatus.interview,
        ApplicationStatus.final_round,
    }])

    offers = len([r for r in records if r.status == ApplicationStatus.offer])
    rejected = len([r for r in records if r.status == ApplicationStatus.rejected])

    pending_followups = len([
        r for r in records
        if r.follow_up_date and r.follow_up_date <= today and r.status not in {
            ApplicationStatus.offer,
            ApplicationStatus.rejected,
        }
    ])

    conversion_rate = 0.0
    if total_applied > 0:
        conversion_rate = round((interviews / total_applied) * 100, 2)

    return TrackerAnalytics(
        total_saved=total_saved,
        total_applied=total_applied,
        interviews_scheduled=interviews,
        offers_received=offers,
        rejected_count=rejected,
        pending_followups=pending_followups,
        application_conversion_rate=conversion_rate,
    )