import json
import logging
from typing import List

from app.schemas.apply import (
    ApplicationAnswer,
    ApplicationPreferenceInput,
    AutoApplyPackageResponse,
)
from app.schemas.job_match import DetailedJob
from app.schemas.profile import SearchProfile
from app.services.llm_service import get_llm
from app.utils.text import clamp_score, truncate_text
from app.core.config import get_settings

logger = logging.getLogger(__name__)


APPLICATION_QUESTIONS = [
    "Why are you interested in this role?",
    "Why should we hire you?",
    "What relevant experience do you have?",
    "What are your strongest skills for this role?",
    "Are you willing to relocate?",
    "What is your notice period?",
    "What are your salary expectations?",
    "Do you have any projects relevant to this role?",
]


def _invoke_text(prompt: str, fallback: str = "") -> str:
    try:
        response = get_llm().invoke(prompt)

        if hasattr(response, "content"):
            return str(response.content).strip()

        return str(response).strip()

    except Exception as exc:
        logger.warning("LLM text generation failed: %s", exc)
        return fallback


def _profile_to_text(profile: SearchProfile) -> str:
    settings = get_settings()
    return truncate_text(profile.to_search_text(), max_chars=settings.max_content_chars)


def _job_to_text(job: DetailedJob) -> str:
    settings = get_settings()

    job_text = "\n".join(
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
            f"Apply URL: {job.apply_url or job.source_url}",
        ]
    )

    return truncate_text(job_text, max_chars=settings.max_content_chars)


def _preferences_to_text(preferences: ApplicationPreferenceInput) -> str:
    return json.dumps(preferences.model_dump(), indent=2)


def _split_lines(text: str) -> List[str]:
    lines = []

    for line in text.splitlines():
        cleaned = line.strip()
        cleaned = cleaned.lstrip("-•*0123456789. ").strip()

        if cleaned:
            lines.append(cleaned)

    return lines


def _fallback_resume_notes(profile: SearchProfile, job: DetailedJob) -> List[str]:
    return [
        f"Align the resume summary more clearly with the {job.title} role.",
        "Move the most relevant technical skills closer to the top of the resume.",
        "Rewrite project bullet points to show measurable technical impact.",
        "Add job-description keywords naturally where they match real experience.",
        "Highlight backend/API/cloud experience more strongly if relevant to the role.",
        "Remove or reduce less relevant details that do not support this application.",
    ]


def _fallback_checklist() -> List[str]:
    return [
        "Review the full job description before applying.",
        "Update the resume summary for this specific role.",
        "Check whether required skills are clearly visible in the resume.",
        "Prepare a short explanation of relevant projects.",
        "Review salary, notice period, and relocation preferences.",
        "Proofread resume and cover letter.",
        "Open the official apply link and review the form.",
        "Submit manually only after final review.",
    ]


def _fallback_risks(job: DetailedJob) -> List[str]:
    return [
        "Some required skills may not be strongly evidenced in the resume.",
        "The resume may need stronger project impact statements.",
        "The application should be reviewed manually before submission.",
        f"The fit depends on how closely the resume supports the {job.title} requirements.",
    ]


def _generate_resume_notes(profile_text: str, job_text: str) -> List[str]:
    prompt = f"""
You are a resume strategist.

Generate exactly 6 practical resume improvement notes for this job application.

Rules:
- Do not invent experience.
- Be specific to the selected job.
- Return only bullet points.
- No introduction.

Candidate profile:
{profile_text}

Selected job:
{job_text}
"""

    text = _invoke_text(prompt)
    notes = _split_lines(text)

    return notes[:6]


def _generate_cover_letter(profile_text: str, job_text: str, preferences_text: str) -> str:
    prompt = f"""
You are a professional cover letter writer.

Write a polished, job-specific cover letter.

Rules:
- 4 short paragraphs.
- Use a professional tone.
- Do not invent experience.
- Use only evidence from the resume/profile and job description.
- If company name is unknown or generic, keep it professional.
- Do not include placeholders except [Your Name] at the end.

Candidate profile:
{profile_text}

Selected job:
{job_text}

User preferences:
{preferences_text}
"""

    return _invoke_text(
        prompt,
        fallback=(
            "Dear Hiring Manager,\n\n"
            "I am interested in applying for this role because it aligns with my technical background and career goals.\n\n"
            "My experience and skills are relevant to the responsibilities described in the job posting, and I would welcome the opportunity to contribute to your team.\n\n"
            "Thank you for considering my application. I would be glad to discuss how my profile fits this role.\n\n"
            "Sincerely,\n[Your Name]"
        ),
    )


def _generate_recruiter_message(profile_text: str, job_text: str) -> str:
    prompt = f"""
Write a concise recruiter message for this job.

Rules:
- 3 to 5 sentences.
- Professional and direct.
- Suitable for LinkedIn or email.
- Do not invent experience.
- No subject line.

Candidate profile:
{profile_text}

Selected job:
{job_text}
"""

    return _invoke_text(
        prompt,
        fallback="Hi, I came across this role and believe my skills align with the requirements. I would be grateful if you could review my profile for this opportunity.",
    )


def _generate_referral_message(profile_text: str, job_text: str) -> str:
    prompt = f"""
Write a referral request message.

Context:
The candidate is asking someone who already works at the company to refer them for this selected job.

Rules:
- The message must be written from the candidate's point of view.
- The candidate is requesting a referral, not giving a referral.
- Be polite, respectful, and not pushy.
- Mention that the candidate found a relevant role at their company.
- Ask if they would be comfortable referring or guiding the candidate.
- Keep it 4 to 6 sentences.
- Suitable for LinkedIn or WhatsApp.
- Do not invent experience.
- Do not say "I would like to refer someone".
- Do not say "if you know anyone who might be interested".
- The message should sound like asking an employee for help.

Candidate profile:
{profile_text}

Selected job:
{job_text}
"""

    return _invoke_text(
        prompt,
        fallback=(
            "Hi, I hope you are doing well. I came across an open role at your company that closely matches my background and skills. "
            "I would be grateful if you could take a quick look and let me know whether you would be comfortable referring me for this position. "
            "I can share my resume and the job link for your review. Thank you for your time."
        ),
    )

def _generate_application_answers(
    profile_text: str,
    job_text: str,
    preferences_text: str,
) -> List[ApplicationAnswer]:
    answers = []

    for question in APPLICATION_QUESTIONS:
        prompt = f"""
Answer this job application question.

Question:
{question}

Rules:
- Answer in 3 to 5 sentences.
- Be specific to the job.
- Do not invent experience.
- If information is not provided, say it can be discussed.
- Do not mention that you are an AI.

Candidate profile:
{profile_text}

Selected job:
{job_text}

User preferences:
{preferences_text}
"""

        answer = _invoke_text(
            prompt,
            fallback="This can be discussed further during the application or interview process.",
        )

        answers.append(ApplicationAnswer(question=question, answer=answer))

    return answers


def _generate_checklist(profile_text: str, job_text: str) -> List[str]:
    prompt = f"""
Generate exactly 8 application checklist items for this selected job.

Rules:
- Return only bullet points.
- Be practical.
- Do not include generic filler.
- Mention resume, cover letter, JD keywords, apply link, and final review.

Candidate profile:
{profile_text}

Selected job:
{job_text}
"""

    text = _invoke_text(prompt)
    checklist = _split_lines(text)

    return checklist[:8]


def _generate_risk_warnings(profile_text: str, job_text: str) -> List[str]:
    prompt = f"""
Generate exactly 4 risk warnings before applying to this job.

Rules:
- Return only bullet points.
- Focus on missing skills, weak proof, resume gaps, and application risks.
- Do not be overly negative.

Candidate profile:
{profile_text}

Selected job:
{job_text}
"""

    text = _invoke_text(prompt)
    risks = _split_lines(text)

    return risks[:4]


def _calculate_readiness_score(
    profile: SearchProfile,
    job: DetailedJob,
    risk_count: int,
) -> float:
    score = 55.0

    profile_skills = {skill.lower() for skill in profile.skills}
    job_skills = {skill.lower() for skill in job.required_skills}

    if job_skills:
        matched = profile_skills.intersection(job_skills)
        score += min(30.0, (len(matched) / max(len(job_skills), 1)) * 30.0)

    if profile.summary:
        score += 5.0

    if profile.certifications:
        score += 5.0

    score -= min(10.0, risk_count * 2.0)

    return clamp_score(score)


def _recommendation_from_score(score: float) -> str:
    if score >= 75:
        return "Apply now"
    if score >= 55:
        return "Apply after minor edits"
    return "Improve profile first"


def generate_auto_apply_package(
    profile: SearchProfile,
    selected_job: DetailedJob,
    preferences: ApplicationPreferenceInput,
) -> AutoApplyPackageResponse:
    profile_text = _profile_to_text(profile)
    job_text = _job_to_text(selected_job)
    preferences_text = _preferences_to_text(preferences)

    resume_notes = _generate_resume_notes(profile_text, job_text)
    if len(resume_notes) < 3:
        resume_notes = _fallback_resume_notes(profile, selected_job)

    cover_letter = _generate_cover_letter(profile_text, job_text, preferences_text)
    recruiter_message = _generate_recruiter_message(profile_text, job_text)
    referral_message = _generate_referral_message(profile_text, job_text)

    application_answers = _generate_application_answers(
        profile_text=profile_text,
        job_text=job_text,
        preferences_text=preferences_text,
    )

    checklist = _generate_checklist(profile_text, job_text)
    if len(checklist) < 3:
        checklist = _fallback_checklist()

    risks = _generate_risk_warnings(profile_text, job_text)
    if len(risks) < 2:
        risks = _fallback_risks(selected_job)

    score = _calculate_readiness_score(profile, selected_job, len(risks))
    final_recommendation = _recommendation_from_score(score)

    return AutoApplyPackageResponse(
        profile=profile,
        selected_job=selected_job,
        apply_readiness_score=score,
        final_recommendation=final_recommendation,
        resume_improvement_notes=resume_notes,
        cover_letter=cover_letter,
        application_answers=application_answers,
        recruiter_message=recruiter_message,
        referral_message=referral_message,
        apply_checklist=checklist,
        risk_warnings=risks,
        apply_url=selected_job.apply_url or selected_job.source_url,
    )


