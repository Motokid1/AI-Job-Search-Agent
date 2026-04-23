import logging
import time
from functools import lru_cache
from http.client import RemoteDisconnected
from typing import Any, Dict, List

from tavily import TavilyClient

from app.core.config import get_settings
from app.utils.text import clean_text, recursive_collect_strings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_tavily_client() -> TavilyClient:
    settings = get_settings()
    return TavilyClient(api_key=settings.tavily_api_key)


def search_web(
    query: str,
    include_domains: List[str] | None = None,
    retries: int = 3,
    delay_seconds: int = 2,
) -> List[Dict[str, Any]]:
    client = get_tavily_client()

    for attempt in range(1, retries + 1):
        try:
            logger.info("Tavily search attempt %d for query: %s", attempt, query)

            response = client.search(
                query=query,
                search_depth="advanced",
                topic="general",
                max_results=get_settings().tavily_max_results,
                include_answer=False,
                include_raw_content=True,
                include_domains=include_domains or None,
            )

            return response.get("results", [])

        except (RemoteDisconnected, ConnectionError, OSError) as exc:
            logger.warning(
                "Tavily search failed on attempt %d for query '%s': %s",
                attempt,
                query,
                exc,
            )
            if attempt < retries:
                time.sleep(delay_seconds)
            else:
                logger.error("Tavily search completely failed for query: %s", query)
                return []

        except Exception as exc:
            logger.warning(
                "Unexpected Tavily search error on attempt %d for query '%s': %s",
                attempt,
                query,
                exc,
            )
            if attempt < retries:
                time.sleep(delay_seconds)
            else:
                logger.error("Tavily search completely failed for query: %s", query)
                return []

    return []


def crawl_url(
    url: str,
    instructions: str,
    retries: int = 2,
    delay_seconds: int = 2,
) -> Dict[str, Any]:
    client = get_tavily_client()

    for attempt in range(1, retries + 1):
        try:
            logger.info("Tavily crawl attempt %d for url: %s", attempt, url)
            response = client.crawl(url=url, instructions=instructions)
            return response

        except Exception as exc:
            logger.warning(
                "Tavily crawl failed on attempt %d for %s: %s",
                attempt,
                url,
                exc,
            )
            if attempt < retries:
                time.sleep(delay_seconds)
            else:
                return {"error": str(exc), "url": url}

    return {"error": "Unknown crawl error", "url": url}


def parse_search_result_content(result: Dict[str, Any]) -> str:
    parts = [
        result.get("title", ""),
        result.get("content", ""),
        result.get("raw_content", ""),
    ]
    return clean_text("\n\n".join([p for p in parts if p]))


def parse_crawl_response_to_text(response: Dict[str, Any]) -> str:
    text_parts = recursive_collect_strings(response)
    return clean_text("\n".join(text_parts))