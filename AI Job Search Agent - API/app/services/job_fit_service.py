from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.config import get_settings
from app.core.prompts import JOB_RESUME_MATCH_PROMPT
from app.schemas.job_match import (
    DetailedJob,
    JobFitGaps,
    JobFitSummary,
    JobResumeImprovements,
    JobResumeMatchResponse,
)
from app.schemas.profile import SearchProfile
from app.services.llm_service import get_llm
from app.services.vectorstore_service import add_documents
from app.utils.text import clamp_score, safe_json_loads


def _profile_to_text(profile: SearchProfile) -> str:
    return profile.to_search_text()


def _job_to_text(job: DetailedJob) -> str:
    return "\n".join(
        [
            f"Title: {job.title}",
            f"Company: {job.company}",
            f"Location: {job.location or ''}",
            f"Salary: {job.salary or ''}",
            f"Experience: {job.experience_text or ''}",
            f"Required Skills: {', '.join(job.required_skills)}",
            f"Tools/Frameworks: {', '.join(job.tools_frameworks)}",
            f"Certifications: {', '.join(job.certifications)}",
            f"Keywords: {', '.join(job.keywords)}",
            f"Responsibilities: {', '.join(job.responsibilities)}",
            f"Summary: {job.summary}",
            f"Description: {job.description}",
        ]
    )


def analyze_resume_against_job(
    profile: SearchProfile,
    detailed_job: DetailedJob,
) -> JobResumeMatchResponse:
    prompt = PromptTemplate.from_template(JOB_RESUME_MATCH_PROMPT)
    chain = prompt | get_llm() | StrOutputParser()

    response_text = chain.invoke(
        {
            "profile_text": _profile_to_text(profile),
            "job_text": _job_to_text(detailed_job),
        }
    )

    data = safe_json_loads(response_text)

    summary_data = data.get("job_fit_summary", {})
    gaps_data = data.get("gaps", {})
    improvements_data = data.get("resume_improvements", {})

    response = JobResumeMatchResponse(
        profile=profile,
        selected_job=detailed_job,
        job_fit_summary=JobFitSummary(
            overall_match_score=clamp_score(summary_data.get("overall_match_score")),
            skills_match_score=clamp_score(summary_data.get("skills_match_score")),
            ats_match_score=clamp_score(summary_data.get("ats_match_score")),
            experience_match_score=clamp_score(summary_data.get("experience_match_score")),
            project_relevance_score=clamp_score(summary_data.get("project_relevance_score")),
            certification_match_score=clamp_score(summary_data.get("certification_match_score")),
            summary=summary_data.get("summary", ""),
        ),
        strengths=data.get("strengths", []),
        gaps=JobFitGaps(
            missing_skills=gaps_data.get("missing_skills", []),
            missing_tools_frameworks=gaps_data.get("missing_tools_frameworks", []),
            missing_keywords=gaps_data.get("missing_keywords", []),
            missing_certifications=gaps_data.get("missing_certifications", []),
            experience_gaps=gaps_data.get("experience_gaps", []),
            project_alignment_issues=gaps_data.get("project_alignment_issues", []),
        ),
        resume_improvements=JobResumeImprovements(
            summary_improvements=improvements_data.get("summary_improvements", []),
            project_bullet_improvements=improvements_data.get("project_bullet_improvements", []),
            keyword_improvements=improvements_data.get("keyword_improvements", []),
            skills_section_improvements=improvements_data.get("skills_section_improvements", []),
        ),
        final_recommendation=data.get("final_recommendation", ""),
    )

    settings = get_settings()
    if settings.enable_chroma_writes:
        add_documents(
            [
                Document(
                    page_content="\n".join(
                        [
                            f"Resume: {profile.summary}",
                            f"Job: {detailed_job.title}",
                            f"Company: {detailed_job.company}",
                            f"Overall Match: {response.job_fit_summary.overall_match_score}",
                            f"Strengths: {', '.join(response.strengths)}",
                            f"Missing Skills: {', '.join(response.gaps.missing_skills)}",
                            f"Recommendation: {response.final_recommendation}",
                        ]
                    ),
                    metadata={
                        "source_url": detailed_job.source_url,
                        "job_title": detailed_job.title,
                        "company": detailed_job.company,
                    },
                )
            ],
            collection_name=settings.chroma_job_match_collection_name,
        )

    return response