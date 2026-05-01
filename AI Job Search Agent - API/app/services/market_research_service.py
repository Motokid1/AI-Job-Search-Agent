import logging
from typing import Dict, List

from app.core.config import get_settings
from app.schemas.analysis import MarketRequirement
from app.schemas.profile import SearchProfile
from app.services.tavily_service import parse_search_result_content, search_web

logger = logging.getLogger(__name__)

BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "reddit.com",
]


def build_market_queries(
    target_role: str,
    package_min_lpa: float | None = None,
    package_max_lpa: float | None = None,
    location: str | None = None,
    companies: list[str] | None = None,
    target_domain: str | None = None,
) -> List[str]:
    package_text = ""
    if package_min_lpa is not None or package_max_lpa is not None:
        package_text = f"{package_min_lpa or ''}-{package_max_lpa or ''} LPA"

    company_text = " ".join((companies or [])[:2])
    location_text = location or ""
    domain_text = target_domain or ""

    queries = [
        f"{target_role} skills requirements {location_text} {company_text}",
        f"{target_role} hiring expectations {package_text} {domain_text}",
    ]

    cleaned = []
    for query in queries:
        q = " ".join(query.split()).strip()
        if q and q not in cleaned:
            cleaned.append(q[:300])

    return cleaned


def collect_market_requirements(
    profile: SearchProfile,
    target_role: str,
    package_min_lpa: float | None = None,
    package_max_lpa: float | None = None,
    companies: list[str] | None = None,
    location: str | None = None,
    target_domain: str | None = None,
) -> List[MarketRequirement]:
    settings = get_settings()

    queries = build_market_queries(
        target_role=target_role,
        package_min_lpa=package_min_lpa,
        package_max_lpa=package_max_lpa,
        location=location,
        companies=companies,
        target_domain=target_domain,
    )

    queries = queries[: settings.max_tavily_queries]

    aggregated_results: Dict[str, dict] = {}

    for query in queries:
        results = search_web(query=query)
        logger.info("Market query '%s' returned %d results", query, len(results))

        for result in results:
            url = result.get("url", "")
            if not url:
                continue

            if any(domain in url.lower() for domain in BLOCKED_DOMAINS):
                continue

            if url not in aggregated_results:
                aggregated_results[url] = result

            if len(aggregated_results) >= settings.max_analysis_market_results:
                break

    requirements: List[MarketRequirement] = []

    for url, result in aggregated_results.items():
        if len(requirements) >= settings.max_analysis_market_results:
            break

        content = parse_search_result_content(result)
        summary = content[:500] if content else f"Market signal for {target_role}."

        requirements.append(
            MarketRequirement(
                role=target_role,
                skills=profile.skills[:],
                tools_frameworks=[],
                certifications=profile.certifications[:],
                experience_expectations=[],
                keywords=profile.skills[:],
                summary=summary,
                source_url=url,
            )
        )

    return requirements