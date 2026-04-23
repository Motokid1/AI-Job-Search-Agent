import logging
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.config import get_settings
from app.core.prompts import LEARNING_RESOURCE_EXTRACTION_PROMPT
from app.schemas.analysis import LearningResource
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


def build_learning_queries(target_role: str, target_domain: str | None = None) -> List[str]:
    domain_text = target_domain or ""
    queries = [
        f"{target_role} github open source projects {domain_text}",
        f"{target_role} official documentation roadmap tutorial",
        f"{target_role} backend learning resources github docs",
    ]

    cleaned = []
    for query in queries:
        q = " ".join(query.split()).strip()
        if q and q not in cleaned:
            cleaned.append(q[:350])
    return cleaned


def _extract_learning_resource(
    target_role: str,
    source_url: str,
    resource_text: str,
    fallback_title: str = "",
) -> LearningResource | None:
    cleaned = truncate_text(resource_text, max_chars=10000)
    if not cleaned:
        return None

    try:
        prompt = PromptTemplate.from_template(LEARNING_RESOURCE_EXTRACTION_PROMPT)
        chain = prompt | get_llm() | StrOutputParser()
        response_text = chain.invoke(
            {
                "target_role": target_role,
                "resource_text": cleaned,
            }
        )

        data = safe_json_loads(response_text)

        return LearningResource(
            title=data.get("title") or fallback_title or "Learning Resource",
            resource_type=data.get("resource_type") or "other",
            skills_covered=normalize_list(data.get("skills_covered", [])),
            summary=data.get("summary", ""),
            difficulty=data.get("difficulty") or "unknown",
            url=source_url,
        )
    except Exception as exc:
        logger.warning("Learning resource extraction failed for %s: %s", source_url, exc)
        return None


def _fallback_learning_resource(
    source_url: str,
    result: Dict[str, Any],
    target_role: str,
) -> LearningResource:
    title = result.get("title") or "Learning Resource"
    content = result.get("content") or result.get("raw_content") or ""
    resource_type = "github" if "github.com" in source_url else "other"

    return LearningResource(
        title=title,
        resource_type=resource_type,
        skills_covered=[target_role],
        summary=content[:250].strip() if content else f"Useful learning resource for {target_role}.",
        difficulty="unknown",
        url=source_url,
    )


def collect_learning_resources(target_role: str, target_domain: str | None = None) -> List[LearningResource]:
    settings = get_settings()
    queries = build_learning_queries(target_role=target_role, target_domain=target_domain)

    aggregated_results: Dict[str, Dict[str, Any]] = {}

    for query in queries:
        results = search_web(query=query)
        logger.info("Learning query '%s' returned %d results", query, len(results))
        for result in results:
            url = result.get("url")
            if not url:
                continue
            if url not in aggregated_results:
                aggregated_results[url] = result

    resources: List[LearningResource] = []

    for idx, (url, result) in enumerate(aggregated_results.items()):
        if len(resources) >= settings.max_resource_results:
            break

        try:
            base_text = parse_search_result_content(result)
            enriched_text = base_text

            crawl_response = crawl_url(
                url=url,
                instructions=(
                    f"Extract why this resource is useful for learning {target_role}, "
                    "what skills it covers, and its likely difficulty level."
                ),
            )
            crawl_text = parse_crawl_response_to_text(crawl_response)

            if crawl_text:
                enriched_text = f"{base_text}\n\n{crawl_text}".strip()

            resource = _extract_learning_resource(
                target_role=target_role,
                source_url=url,
                resource_text=enriched_text,
                fallback_title=result.get("title", "") or f"Resource {idx + 1}",
            )

            if not resource:
                resource = _fallback_learning_resource(url, result, target_role)

            resources.append(resource)

        except Exception as exc:
            logger.warning("Failed to process learning resource from %s: %s", url, exc)

    if resources:
        docs = []
        for item in resources:
            docs.append(
                Document(
                    page_content="\n".join(
                        [
                            f"Title: {item.title}",
                            f"Type: {item.resource_type}",
                            f"Skills: {', '.join(item.skills_covered)}",
                            f"Difficulty: {item.difficulty}",
                            f"Summary: {item.summary}",
                        ]
                    ),
                    metadata={"source_url": item.url, "type": item.resource_type},
                )
            )
        add_documents(docs, collection_name=settings.chroma_resource_collection_name)

    return resources