import json
import re
from typing import Any, Dict, Iterable, List


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 12000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars]


def safe_json_loads(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1).strip()

    return json.loads(text)


def normalize_list(values: Iterable[str]) -> List[str]:
    seen = set()
    output = []

    for value in values:
        item = str(value).strip()
        if not item:
            continue
        key = item.lower()
        if key not in seen:
            seen.add(key)
            output.append(item)

    return output


def recursive_collect_strings(value: Any) -> List[str]:
    collected: List[str] = []

    if isinstance(value, str):
        collected.append(value)
    elif isinstance(value, dict):
        for nested in value.values():
            collected.extend(recursive_collect_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            collected.extend(recursive_collect_strings(nested))

    return collected


def clamp_score(value: Any, minimum: float = 0.0, maximum: float = 100.0) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = minimum
    return round(max(minimum, min(maximum, numeric)), 2)