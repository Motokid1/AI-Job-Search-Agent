import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.core.prompts import RESUME_ANALYSIS_PROMPT
from app.schemas.analysis import (
    CareerGrowthSuggestions,
    FitAnalysis,
    GapReport,
    LearningResource,
    MarketRequirement,
    ResumeAnalysisResponse,
    ResumeModifications,
)
from app.schemas.profile import SearchProfile
from app.services.llm_service import get_llm
from app.utils.text import clamp_score, safe_json_loads

logger = logging.getLogger(__name__)


def _profile_to_text(profile: SearchProfile) -> str:
    return profile.to_search_text()


def _market_to_text(requirements: list[MarketRequirement]) -> str:
    if not requirements:
        return "No market requirements found."

    lines = []
    for item in requirements:
        lines.extend(
            [
                f"Role: {item.role}",
                f"Skills: {', '.join(item.skills)}",
                f"Tools/Frameworks: {', '.join(item.tools_frameworks)}",
                f"Certifications: {', '.join(item.certifications)}",
                f"Experience Expectations: {', '.join(item.experience_expectations)}",
                f"Keywords: {', '.join(item.keywords)}",
                f"Summary: {item.summary}",
                f"Source: {item.source_url}",
                "",
            ]
        )
    return "\n".join(lines)


def _resources_to_text(resources: list[LearningResource]) -> str:
    if not resources:
        return "No learning resources found."

    lines = []
    for item in resources:
        lines.extend(
            [
                f"Title: {item.title}",
                f"Type: {item.resource_type}",
                f"Skills Covered: {', '.join(item.skills_covered)}",
                f"Difficulty: {item.difficulty}",
                f"Summary: {item.summary}",
                f"URL: {item.url}",
                "",
            ]
        )
    return "\n".join(lines)


def generate_resume_analysis(
    profile: SearchProfile,
    target_role: str,
    package_min_lpa: float | None,
    package_max_lpa: float | None,
    location: str | None,
    companies: list[str],
    target_domain: str | None,
    market_requirements: list[MarketRequirement],
    learning_resources: list[LearningResource],
) -> ResumeAnalysisResponse:
    prompt = PromptTemplate.from_template(RESUME_ANALYSIS_PROMPT)
    chain = prompt | get_llm() | StrOutputParser()

    response_text = chain.invoke(
        {
            "profile_text": _profile_to_text(profile),
            "market_text": _market_to_text(market_requirements),
            "resource_text": _resources_to_text(learning_resources),
        }
    )

    data = safe_json_loads(response_text)

    fit_data = data.get("fit_analysis", {})
    gap_data = data.get("gap_report", {})
    resume_mod_data = data.get("resume_modifications", {})
    growth_data = data.get("career_growth_suggestions", {})

    fit_analysis = FitAnalysis(
        resume_strength_score=clamp_score(fit_data.get("resume_strength_score")),
        role_readiness_score=clamp_score(fit_data.get("role_readiness_score")),
        package_readiness_score=clamp_score(fit_data.get("package_readiness_score")),
        ats_score=clamp_score(fit_data.get("ats_score")),
        strengths=fit_data.get("strengths", []),
        overall_summary=fit_data.get("overall_summary", ""),
    )

    gap_report = GapReport(
        missing_skills=gap_data.get("missing_skills", []),
        missing_tools_frameworks=gap_data.get("missing_tools_frameworks", []),
        missing_certifications=gap_data.get("missing_certifications", []),
        weak_projects=gap_data.get("weak_projects", []),
        weak_keywords=gap_data.get("weak_keywords", []),
        experience_gap=gap_data.get("experience_gap", ""),
    )

    resume_modifications = ResumeModifications(
        summary_suggestions=resume_mod_data.get("summary_suggestions", []),
        project_rewrite_suggestions=resume_mod_data.get("project_rewrite_suggestions", []),
        skills_section_improvements=resume_mod_data.get("skills_section_improvements", []),
        missing_sections=resume_mod_data.get("missing_sections", []),
        ats_keyword_improvements=resume_mod_data.get("ats_keyword_improvements", []),
    )

    career_growth = CareerGrowthSuggestions(
        skills_to_learn_next=growth_data.get("skills_to_learn_next", []),
        certifications_to_consider=growth_data.get("certifications_to_consider", []),
        projects_to_build=growth_data.get("projects_to_build", []),
        interview_topics=growth_data.get("interview_topics", []),
    )

    return ResumeAnalysisResponse(
        profile=profile,
        target_role=target_role,
        package_min_lpa=package_min_lpa,
        package_max_lpa=package_max_lpa,
        location=location,
        companies=companies,
        target_domain=target_domain,
        market_requirements=market_requirements,
        learning_resources=learning_resources,
        fit_analysis=fit_analysis,
        gap_report=gap_report,
        resume_modifications=resume_modifications,
        career_growth_suggestions=career_growth,
        final_recommendation=data.get("final_recommendation", ""),
    )