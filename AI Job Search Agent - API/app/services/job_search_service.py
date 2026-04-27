import logging
from typing import Any, Dict, List
from urllib.parse import urlparse

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.config import get_settings
from app.core.prompts import JOB_EXTRACTION_PROMPT
from app.schemas.job import JobPosting, SearchResponse
from app.schemas.profile import SearchProfile
from app.services.llm_service import get_llm
from app.services.matching_service import compute_match
from app.services.tavily_service import (
    crawl_url,
    parse_crawl_response_to_text,
    parse_search_result_content,
    search_web,
)
from app.services.vectorstore_service import add_job_documents, similarity_search
from app.utils.text import normalize_list, safe_json_loads, truncate_text

logger = logging.getLogger(__name__)


def build_search_queries(profile: SearchProfile) -> List[str]:
    queries: List[str] = []

    skill_part = " ".join(profile.skills[:6]) if profile.skills else ""
    role_part = profile.desired_role or "software engineer"
    exp_part = (
        f"{int(profile.years_experience)} years experience"
        if profile.years_experience is not None
        else ""
    )
    location_part = profile.location or ""
    company_part = " ".join(profile.companies[:3]) if profile.companies else ""

    queries.append(f"{role_part} {skill_part} {exp_part} {location_part} jobs careers")
    queries.append(f"{skill_part} {location_part} hiring {company_part} careers")
    queries.append(f"{role_part} {location_part} job opening apply")

    cleaned = []
    for query in queries:
        q = " ".join(query.split()).strip()
        if q and q not in cleaned:
            cleaned.append(q[:350])

    return cleaned


def _extract_job_from_content(
    profile: SearchProfile,
    source_url: str,
    raw_text: str,
    fallback_title: str = "",
) -> JobPosting | None:
    cleaned = truncate_text(raw_text, max_chars=12000)
    if not cleaned:
        return None

    try:
        prompt = PromptTemplate.from_template(JOB_EXTRACTION_PROMPT)
        chain = prompt | get_llm() | StrOutputParser()
        response_text = chain.invoke(
            {
                "profile_text": profile.to_search_text(),
                "job_text": cleaned,
            }
        )

        data = safe_json_loads(response_text)

        title = data.get("title") or fallback_title or "Unknown Title"
        company = data.get("company") or urlparse(source_url).netloc.replace("www.", "")

        return JobPosting(
            title=title,
            company=company,
            location=data.get("location"),
            salary=data.get("salary"),
            experience_text=data.get("experience_text"),
            required_skills=normalize_list(data.get("required_skills", [])),
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            apply_url=data.get("apply_url") or source_url,
            source_url=source_url,
        )

    except Exception as exc:
        logger.warning("LLM extraction failed for %s: %s", source_url, exc)
        return None


def _build_documents_for_chroma(jobs: List[JobPosting]) -> List[Document]:
    docs: List[Document] = []
    for job in jobs:
        page_content = "\n".join(
            [
                f"Title: {job.title}",
                f"Company: {job.company}",
                f"Location: {job.location or ''}",
                f"Salary: {job.salary or ''}",
                f"Experience: {job.experience_text or ''}",
                f"Skills: {', '.join(job.required_skills)}",
                f"Summary: {job.summary}",
                f"Description: {job.description}",
            ]
        )

        docs.append(
            Document(
                page_content=page_content,
                metadata={
                    "source_url": job.source_url,
                    "company": job.company,
                    "title": job.title,
                    "location": job.location or "",
                    "apply_url": job.apply_url or "",
                },
            )
        )
    return docs


def search_jobs_for_profile(profile: SearchProfile) -> SearchResponse:
    settings = get_settings()
    queries = build_search_queries(profile)

    aggregated_results: Dict[str, Dict[str, Any]] = {}
    include_domains = None

    # -----------------------------
    # STEP 1: Tavily Search
    # -----------------------------
    for query in queries:
        try:
            results = search_web(query=query, include_domains=include_domains)
            logger.info("Query '%s' returned %d results", query, len(results))

            for result in results:
                url = result.get("url")
                if not url:
                    continue

                if url not in aggregated_results:
                    aggregated_results[url] = result

        except Exception as exc:
            logger.warning("Skipping failed query '%s': %s", query, exc)
            continue

    logger.info("Collected %d unique search results", len(aggregated_results))

    # -----------------------------
    # STEP 2: Crawl + Extract Jobs
    # -----------------------------
    jobs: List[JobPosting] = []
    crawled_count = 0
    MAX_JOBS = 2

    for url, result in aggregated_results.items():
        if len(jobs) >= MAX_JOBS:
            logger.info("Reached max job limit (%d), stopping further processing", MAX_JOBS)
            break

        try:
            base_text = parse_search_result_content(result)
            enriched_text = base_text

            if crawled_count < settings.max_crawl_urls:
                instructions = (
                    "Extract the page details for a job posting or career opportunity. "
                    "Focus on role title, company, location, skills, salary, "
                    "experience, and apply link. "
                    f"Candidate profile context: {profile.to_search_text()}"
                )

                crawl_response = crawl_url(url=url, instructions=instructions)
                crawl_text = parse_crawl_response_to_text(crawl_response)

                if crawl_text:
                    enriched_text = f"{base_text}\n\n{crawl_text}".strip()

                crawled_count += 1

            job = _extract_job_from_content(
                profile=profile,
                source_url=url,
                raw_text=enriched_text,
                fallback_title=result.get("title", ""),
            )

            # Fallback if LLM extraction fails
            if not job:
                logger.info("Using fallback job builder for %s", url)
                job = _build_fallback_job_from_result(result, profile)

            if job:
                job = compute_match(job, profile)
                jobs.append(job)
                logger.info("Added job %d/%d: %s", len(jobs), MAX_JOBS, job.title)

        except Exception as exc:
            logger.warning("Failed to process result from %s: %s", url, exc)
            continue

    if not jobs:
        logger.warning("No jobs could be extracted after search/crawl stage")

    # Optional Chroma store
    if jobs:
        try:
            add_job_documents(_build_documents_for_chroma(jobs))
        except Exception as exc:
            logger.warning("Failed to add job documents to Chroma: %s", exc)

    # For now, return directly after compute_match
    jobs.sort(key=lambda item: item.match_score, reverse=True)

    logger.info("Returning %d jobs directly to frontend", len(jobs))

    return SearchResponse(
        profile=profile,
        total_found=len(jobs),
        jobs=jobs,
    )

def _build_fallback_job_from_result(
    result: Dict[str, Any],
    profile: SearchProfile,
) -> JobPosting | None:
    url = result.get("url")
    title = result.get("title") or "Job Opportunity"
    content = result.get("content") or result.get("raw_content") or ""

    if not url:
        return None

    company = "Unknown Company"
    if " - " in title:
        company = title.split(" - ")[-1].strip()
    elif "|" in title:
        company = title.split("|")[-1].strip()

    summary = content[:300].strip() if content else "Relevant job result found from Tavily search."

    job = JobPosting(
        title=title,
        company=company,
        location=profile.location,
        salary=None,
        experience_text=None,
        required_skills=profile.skills[:],
        summary=summary,
        description=content[:1500] if content else summary,
        apply_url=url,
        source_url=url,
    )
    return job