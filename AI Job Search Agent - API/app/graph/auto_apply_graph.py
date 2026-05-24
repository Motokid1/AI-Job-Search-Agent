from typing import Any, Dict, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.schemas.auto_apply_runtime import AutoApplyStatus
from app.services.auto_apply_session_store import get_session, update_session


class AutoApplyState(TypedDict, total=False):
    session_id: str
    decision: str


def load_context(state: AutoApplyState) -> AutoApplyState:
    session = get_session(state["session_id"])

    if not session:
        raise ValueError("Auto apply session not found.")

    update_session(
        state["session_id"],
        {
            "status": AutoApplyStatus.created,
            "current_step": "load_context",
            "message": "Loaded auto-apply session.",
        },
    )

    return state


def open_browser(state: AutoApplyState) -> AutoApplyState:
    session = get_session(state["session_id"])
    browser = session["browser"]
    job_url = session["job_url"]

    update_session(
        state["session_id"],
        {
            "status": AutoApplyStatus.opening_browser,
            "current_step": "open_browser",
            "message": "Opening application page.",
        },
    )

    browser_url = browser.open(job_url)
    blocker = browser.detect_blockers()

    if blocker:
        update_session(
            state["session_id"],
            {
                "status": AutoApplyStatus.blocked,
                "current_step": "blocked",
                "message": blocker,
                "browser_url": browser_url,
                "requires_user_action": True,
            },
        )
        return state

    update_session(
        state["session_id"],
        {
            "browser_url": browser_url,
            "message": "Application page opened.",
        },
    )

    return state


def inspect_form(state: AutoApplyState) -> AutoApplyState:
    session = get_session(state["session_id"])
    browser = session["browser"]

    fields = browser.inspect_fields()

    update_session(
        state["session_id"],
        {
            "status": AutoApplyStatus.form_detected,
            "current_step": "inspect_form",
            "message": f"Detected {len(fields)} form fields.",
            "detected_fields": fields,
        },
    )

    return state


def fill_form(state: AutoApplyState) -> AutoApplyState:
    session = get_session(state["session_id"])
    browser = session["browser"]
    candidate = session["candidate"]

    update_session(
        state["session_id"],
        {
            "status": AutoApplyStatus.filling_form,
            "current_step": "fill_form",
            "message": "Filling known application fields.",
        },
    )

    filled_fields = browser.fill_fields(candidate)
    resume_uploaded = browser.upload_resume(session["resume_path"])

    update_session(
        state["session_id"],
        {
            "status": AutoApplyStatus.waiting_for_approval,
            "current_step": "human_review_interrupt",
            "message": "Application form is filled. Please review before submission.",
            "filled_fields": filled_fields,
            "resume_uploaded": resume_uploaded,
            "requires_user_action": True,
        },
    )

    return state


def human_review_interrupt(state: AutoApplyState) -> AutoApplyState:
    decision_payload = interrupt(
        {
            "message": "Application form is filled. Review the browser and choose submit or cancel.",
            "options": ["submit", "cancel", "manual_review"],
        }
    )

    state["decision"] = decision_payload.get("decision", "manual_review")
    return state


def submit_or_cancel(state: AutoApplyState) -> AutoApplyState:
    session = get_session(state["session_id"])
    browser = session["browser"]
    decision = state.get("decision", "manual_review")

    if decision == "submit":
        submitted = browser.submit_application()

        if submitted:
            update_session(
                state["session_id"],
                {
                    "status": AutoApplyStatus.submitted,
                    "current_step": "submitted",
                    "message": "Application submitted successfully.",
                    "requires_user_action": False,
                },
            )
        else:
            update_session(
                state["session_id"],
                {
                    "status": AutoApplyStatus.failed,
                    "current_step": "submit_failed",
                    "message": "Could not find or click submit button. Please continue manually.",
                    "requires_user_action": True,
                },
            )

    elif decision == "cancel":
        browser.close()
        update_session(
            state["session_id"],
            {
                "status": AutoApplyStatus.cancelled,
                "current_step": "cancelled",
                "message": "Auto apply session cancelled.",
                "requires_user_action": False,
            },
        )

    else:
        update_session(
            state["session_id"],
            {
                "status": AutoApplyStatus.waiting_for_approval,
                "current_step": "manual_review",
                "message": "Browser remains open for manual review.",
                "requires_user_action": True,
            },
        )

    return state


def build_auto_apply_graph():
    graph = StateGraph(AutoApplyState)

    graph.add_node("load_context", load_context)
    graph.add_node("open_browser", open_browser)
    graph.add_node("inspect_form", inspect_form)
    graph.add_node("fill_form", fill_form)
    graph.add_node("human_review_interrupt", human_review_interrupt)
    graph.add_node("submit_or_cancel", submit_or_cancel)

    graph.add_edge(START, "load_context")
    graph.add_edge("load_context", "open_browser")
    graph.add_edge("open_browser", "inspect_form")
    graph.add_edge("inspect_form", "fill_form")
    graph.add_edge("fill_form", "human_review_interrupt")
    graph.add_edge("human_review_interrupt", "submit_or_cancel")
    graph.add_edge("submit_or_cancel", END)

    return graph.compile()