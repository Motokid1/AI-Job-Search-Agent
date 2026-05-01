import logging
from typing import Dict, List

from app.core.config import get_settings
from app.schemas.analysis import LearningResource
from app.services.tavily_service import search_web

logger = logging.getLogger(__name__)

BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "reddit.com",
]


def build_learning_queries(target_role: str, target_domain: str | None = None) -> List[str]:
    domain_text = target_domain or ""

    queries = [
        f"{target_role} github open source projects {domain_text}",
        f"{target_role} documentation roadmap tutorial",
    ]

    cleaned = []
    for query in queries:
        q = " ".join(query.split()).strip()
        if q and q not in cleaned:
            cleaned.append(q[:300])

    return cleaned


def collect_learning_resources(
    target_role: str,
    target_domain: str | None = None,
) -> List[LearningResource]:
    settings = get_settings()

    queries = build_learning_queries(target_role=target_role, target_domain=target_domain)
    queries = queries[: settings.max_tavily_queries]

    aggregated_results: Dict[str, dict] = {}

    for query in queries:
        results = search_web(query=query)
        logger.info("Learning query '%s' returned %d results", query, len(results))

        for result in results:
            url = result.get("url", "")
            if not url:
                continue

            if any(domain in url.lower() for domain in BLOCKED_DOMAINS):
                continue

            if url not in aggregated_results:
                aggregated_results[url] = result

            if len(aggregated_results) >= settings.max_resource_results:
                break

    resources: List[LearningResource] = []

    for url, result in aggregated_results.items():
        if len(resources) >= settings.max_resource_results:
            break

        title = result.get("title") or "Learning Resource"
        content = result.get("content") or ""

        resources.append(
            LearningResource(
                title=title,
                resource_type="github" if "github.com" in url else "other",
                skills_covered=[target_role],
                summary=content[:300] if content else f"Useful resource for {target_role}.",
                difficulty="unknown",
                url=url,
            )
        )

    return resources