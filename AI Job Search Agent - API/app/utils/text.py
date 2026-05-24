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


def _extract_json_object(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found in LLM response.")

    return text[start : end + 1]


def _escape_control_chars_inside_strings(text: str) -> str:
    result = []
    in_string = False
    escape = False

    for char in text:
        if escape:
            result.append(char)
            escape = False
            continue

        if char == "\\":
            result.append(char)
            escape = True
            continue

        if char == '"':
            result.append(char)
            in_string = not in_string
            continue

        if in_string:
            if char == "\n":
                result.append("\\n")
            elif char == "\r":
                result.append("\\r")
            elif char == "\t":
                result.append("\\t")
            else:
                result.append(char)
        else:
            result.append(char)

    return "".join(result)


def safe_json_loads(text: str) -> Dict[str, Any]:
    json_text = _extract_json_object(text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        repaired = _escape_control_chars_inside_strings(json_text)
        return json.loads(repaired)


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