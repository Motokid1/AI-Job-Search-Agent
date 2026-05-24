from typing import Any, Dict


AUTO_APPLY_SESSIONS: Dict[str, Dict[str, Any]] = {}


def create_session(session_id: str, data: Dict[str, Any]) -> None:
    AUTO_APPLY_SESSIONS[session_id] = data


def get_session(session_id: str) -> Dict[str, Any] | None:
    return AUTO_APPLY_SESSIONS.get(session_id)


def update_session(session_id: str, updates: Dict[str, Any]) -> None:
    if session_id in AUTO_APPLY_SESSIONS:
        AUTO_APPLY_SESSIONS[session_id].update(updates)


def delete_session(session_id: str) -> None:
    AUTO_APPLY_SESSIONS.pop(session_id, None)