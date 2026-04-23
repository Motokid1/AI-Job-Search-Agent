from typing import List

from app.schemas.job import JobPosting
from app.schemas.profile import SearchProfile


def compute_match(job: JobPosting, profile: SearchProfile) -> JobPosting:
    score = 0.0
    reasons: List[str] = []
    missing_skills: List[str] = []

    profile_skills_lower = {skill.lower() for skill in profile.skills}
    job_skills_lower = {skill.lower() for skill in job.required_skills}

    matched_skills = profile_skills_lower.intersection(job_skills_lower)

    if matched_skills:
        skill_score = min(50.0, len(matched_skills) * 10.0)
        score += skill_score
        reasons.append(f"Matched skills: {', '.join(sorted(matched_skills))}")

    for skill in job_skills_lower:
        if skill not in profile_skills_lower:
            missing_skills.append(skill)

    if profile.location and job.location:
        if profile.location.lower() in job.location.lower():
            score += 15.0
            reasons.append("Preferred location matched")

    if profile.desired_role and job.title:
        if profile.desired_role.lower() in job.title.lower():
            score += 20.0
            reasons.append("Desired role matched with job title")

    if profile.companies and job.company:
        company_matches = [c for c in profile.companies if c.lower() in job.company.lower()]
        if company_matches:
            score += 10.0
            reasons.append(f"Preferred company matched: {', '.join(company_matches)}")

    if profile.years_experience is not None and job.experience_text:
        reasons.append(f"Candidate experience: {profile.years_experience} years")

    job.match_score = round(min(score, 100.0), 2)
    job.match_reasons = reasons
    job.missing_skills = sorted(set(missing_skills))
    return job