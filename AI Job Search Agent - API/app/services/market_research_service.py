import logging
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.config import get_settings
from app.core.prompts import MARKET_REQUIREMENT_EXTRACTION_PROMPT
from app.schemas.analysis import MarketRequirement
from app.schemas.profile import SearchProfile
from app.services.llm_service import get_llm
from app.services.tavily_service import (
    crawl_url,
    parse_crawl_response_to_text,
    parse_search_result_content,
    search_web,
)
from app.services.vectorstore_service import add_documents
from app.utils.text import normalize_list, safe_json_loads, truncate_text

logger = logging.getLogger(__name__)


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

    company_text = " ".join((companies or [])[:3])
    location_text = location or ""
    domain_text = target_domain or ""

    queries = [
        f"{target_role} skills requirements {location_text} {company_text}",
        f"{target_role} hiring expectations {package_text} {location_text}",
        f"{target_role} tools frameworks responsibilities {domain_text}",
    ]

    cleaned = []
    for query in queries:
        q = " ".join(query.split()).strip()
        if q and q not in cleaned:
            cleaned.append(q[:350])
    return cleaned


def _extract_market_requirement(
    target_role: str,
    package_text: str,
    source_url: str,
    market_text: str,
    fallback_title: str = "",
) -> MarketRequirement | None:
    cleaned = truncate_text(market_text, max_chars=12000)
    if not cleaned:
        return None

    try:
        prompt = PromptTemplate.from_template(MARKET_REQUIREMENT_EXTRACTION_PROMPT)
        chain = prompt | get_llm() | StrOutputParser()
        response_text = chain.invoke(
            {
                "target_role": target_role,
                "package_text": package_text or "Not specified",
                "market_text": cleaned,
            }
        )

        data = safe_json_loads(response_text)

        return MarketRequirement(
            role=data.get("role") or fallback_title or target_role,
            skills=normalize_list(data.get("skills", [])),
            tools_frameworks=normalize_list(data.get("tools_frameworks", [])),
            certifications=normalize_list(data.get("certifications", [])),
            experience_expectations=normalize_list(data.get("experience_expectations", [])),
            keywords=normalize_list(data.get("keywords", [])),
            summary=data.get("summary", ""),
            source_url=source_url,
        )
    except Exception as exc:
        logger.warning("Market requirement extraction failed for %s: %s", source_url, exc)
        return None


def _fallback_market_requirement(
    target_role: str,
    source_url: str,
    result: Dict[str, Any],
    profile: SearchProfile,
) -> MarketRequirement:
    content = result.get("content") or result.get("raw_content") or ""
    return MarketRequirement(
        role=target_role,
        skills=profile.skills[:],
        tools_frameworks=[],
        certifications=profile.certifications[:],
        experience_expectations=[],
        keywords=profile.skills[:],
        summary=(content[:300].strip() if content else f"Relevant market signal for {target_role}."),
        source_url=source_url,
    )


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

    aggregated_results: Dict[str, Dict[str, Any]] = {}
    for query in queries:
        results = search_web(query=query)
        logger.info("Market query '%s' returned %d results", query, len(results))
        for result in results:
            url = result.get("url")
            if not url:
                continue
            if url not in aggregated_results:
                aggregated_results[url] = result

    requirements: List[MarketRequirement] = []
    package_text = (
        f"{package_min_lpa or ''}-{package_max_lpa or ''} LPA"
        if package_min_lpa is not None or package_max_lpa is not None
        else "Not specified"
    )

    for idx, (url, result) in enumerate(aggregated_results.items()):
        if len(requirements) >= settings.max_analysis_market_results:
            break

        try:
            base_text = parse_search_result_content(result)
            enriched_text = base_text

            crawl_response = crawl_url(
                url=url,
                instructions=(
                    "Extract role requirements, key skills, tools, certifications, experience expectations, "
                    f"and important hiring keywords for {target_role}."
                ),
            )
            crawl_text = parse_crawl_response_to_text(crawl_response)

            if crawl_text:
                enriched_text = f"{base_text}\n\n{crawl_text}".strip()

            requirement = _extract_market_requirement(
                target_role=target_role,
                package_text=package_text,
                source_url=url,
                market_text=enriched_text,
                fallback_title=result.get("title", "") or f"{target_role} Requirement {idx + 1}",
            )

            if not requirement:
                requirement = _fallback_market_requirement(
                    target_role=target_role,
                    source_url=url,
                    result=result,
                    profile=profile,
                )

            requirements.append(requirement)

        except Exception as exc:
            logger.warning("Failed to collect market requirement from %s: %s", url, exc)

    if requirements:
        docs = []
        settings = get_settings()
        for item in requirements:
            docs.append(
                Document(
                    page_content="\n".join(
                        [
                            f"Role: {item.role}",
                            f"Skills: {', '.join(item.skills)}",
                            f"Tools/Frameworks: {', '.join(item.tools_frameworks)}",
                            f"Certifications: {', '.join(item.certifications)}",
                            f"Experience: {', '.join(item.experience_expectations)}",
                            f"Keywords: {', '.join(item.keywords)}",
                            f"Summary: {item.summary}",
                        ]
                    ),
                    metadata={"source_url": item.source_url, "role": item.role},
                )
            )
        add_documents(docs, collection_name=settings.chroma_analysis_collection_name)

    return requirements