import logging
import time
from functools import lru_cache
from typing import Any, Dict, List

from tavily import TavilyClient

from app.core.config import get_settings
from app.utils.text import clean_text, recursive_collect_strings

logger = logging.getLogger(__name__)

BLOCKED_CRAWL_DOMAINS = [
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "medium.com",
    "reddit.com",
]


@lru_cache(maxsize=1)
def get_tavily_client() -> TavilyClient:
    settings = get_settings()
    return TavilyClient(api_key=settings.tavily_api_key)


def search_web(
    query: str,
    include_domains: List[str] | None = None,
    retries: int = 2,
    delay_seconds: int = 1,
) -> List[Dict[str, Any]]:
    client = get_tavily_client()
    settings = get_settings()

    for attempt in range(1, retries + 1):
        try:
            logger.info("Tavily search attempt %d for query: %s", attempt, query)

            response = client.search(
                query=query,
                search_depth="basic",
                topic="general",
                max_results=min(settings.tavily_max_results, settings.max_search_results),
                include_answer=False,
                include_raw_content=False,
                include_domains=include_domains or None,
            )

            return response.get("results", [])

        except Exception as exc:
            logger.warning(
                "Tavily search failed on attempt %d for query '%s': %s",
                attempt,
                query,
                exc,
            )

            if attempt < retries:
                time.sleep(delay_seconds)
            else:
                return []

    return []


def crawl_url(
    url: str,
    instructions: str,
    retries: int = 1,
    delay_seconds: int = 1,
    force: bool = False,
) -> Dict[str, Any]:
    settings = get_settings()

    if not force and not settings.enable_job_crawling:
        logger.info("Crawling disabled. Skipping crawl for: %s", url)
        return {"url": url, "skipped": True, "reason": "Crawling disabled"}

    if any(domain in url.lower() for domain in BLOCKED_CRAWL_DOMAINS):
        logger.info("Skipping crawl for blocked domain: %s", url)
        return {"url": url, "skipped": True, "reason": "Blocked slow domain"}

    client = get_tavily_client()

    for attempt in range(1, retries + 1):
        try:
            logger.info("Tavily crawl attempt %d for url: %s", attempt, url)
            return client.crawl(url=url, instructions=instructions)

        except Exception as exc:
            logger.warning("Tavily crawl failed for %s: %s", url, exc)

            if attempt < retries:
                time.sleep(delay_seconds)
            else:
                return {"error": str(exc), "url": url}

    return {"error": "Unknown crawl error", "url": url}


def parse_search_result_content(result: Dict[str, Any]) -> str:
    parts = [
        result.get("title", ""),
        result.get("content", ""),
    ]
    return clean_text("\n\n".join([p for p in parts if p]))


def parse_crawl_response_to_text(response: Dict[str, Any]) -> str:
    text_parts = recursive_collect_strings(response)
    return clean_text("\n".join(text_parts))