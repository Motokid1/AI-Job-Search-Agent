import logging
from urllib.parse import urlparse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.prompts import JOB_DETAIL_EXTRACTION_PROMPT
from app.schemas.job_match import DetailedJob, SelectedJobInput
from app.services.llm_service import get_llm
from app.services.tavily_service import crawl_url, parse_crawl_response_to_text
from app.utils.text import normalize_list, safe_json_loads, truncate_text

logger = logging.getLogger(__name__)


def _fallback_detailed_job(job: SelectedJobInput, crawled_text: str) -> DetailedJob:
    return DetailedJob(
        title=job.title,
        company=job.company,
        location=job.location,
        salary=None,
        experience_text=None,
        required_skills=normalize_list(job.required_skills),
        tools_frameworks=[],
        certifications=[],
        keywords=normalize_list(job.required_skills),
        summary=job.summary or "Selected job details fetched from source.",
        description=(crawled_text[:3000] if crawled_text else (job.description or job.summary or "")),
        responsibilities=[],
        apply_url=job.apply_url or job.source_url,
        source_url=job.source_url,
    )


def fetch_detailed_job(job: SelectedJobInput) -> DetailedJob:
    instructions = (
        "Extract the complete job description, required skills, tools/frameworks, certifications, "
        "keywords, responsibilities, experience requirements, salary if available, and apply link."
    )

    crawl_response = crawl_url(url=job.source_url, instructions=instructions)
    crawl_text = parse_crawl_response_to_text(crawl_response)
    cleaned_text = truncate_text(crawl_text or job.description or job.summary or "", max_chars=12000)

    if not cleaned_text:
        return _fallback_detailed_job(job, "")

    try:
        prompt = PromptTemplate.from_template(JOB_DETAIL_EXTRACTION_PROMPT)
        chain = prompt | get_llm() | StrOutputParser()
        response_text = chain.invoke({"job_text": cleaned_text})
        data = safe_json_loads(response_text)

        return DetailedJob(
            title=data.get("title") or job.title,
            company=data.get("company") or job.company or urlparse(job.source_url).netloc.replace("www.", ""),
            location=data.get("location") or job.location,
            salary=data.get("salary"),
            experience_text=data.get("experience_text"),
            required_skills=normalize_list(data.get("required_skills", []) or job.required_skills),
            tools_frameworks=normalize_list(data.get("tools_frameworks", [])),
            certifications=normalize_list(data.get("certifications", [])),
            keywords=normalize_list(data.get("keywords", [])),
            summary=data.get("summary", "") or job.summary or "",
            description=data.get("description", "") or cleaned_text[:3000],
            responsibilities=normalize_list(data.get("responsibilities", [])),
            apply_url=data.get("apply_url") or job.apply_url or job.source_url,
            source_url=job.source_url,
        )

    except Exception as exc:
        logger.warning("Detailed job extraction failed for %s: %s", job.source_url, exc)
        return _fallback_detailed_job(job, cleaned_text)