PROFILE_EXTRACTION_PROMPT = """
You are an expert resume parser.

Extract structured information from the resume text below.

Return ONLY valid JSON with this exact schema:
{{
  "desired_role": "string or null",
  "skills": ["string", "..."],
  "years_experience": number or null,
  "certifications": ["string", "..."],
  "location": "string or null",
  "projects": ["string", "..."],
  "summary": "short professional summary"
}}

Rules:
- Do not add extra keys.
- skills must be concise and deduplicated.
- years_experience should be numeric if inferable, else null.
- certifications should only contain explicit certifications.
- summary should be 2-4 lines in plain text.
- If a field is not available, return null or [].

Resume text:
{resume_text}
"""


JOB_EXTRACTION_PROMPT = """
You are an AI job information extractor.

Given the following web content for a job/career page and the candidate profile, extract one job posting.

Return ONLY valid JSON with this exact schema:
{{
  "title": "string",
  "company": "string",
  "location": "string or null",
  "salary": "string or null",
  "experience_text": "string or null",
  "required_skills": ["string", "..."],
  "summary": "short summary",
  "description": "cleaned description",
  "apply_url": "string or null"
}}

Rules:
- Return one best job interpretation from the text.
- If title/company is missing, infer carefully from context if possible.
- required_skills must be concise and deduplicated.
- description should be useful but not too long.
- summary should be 2-4 lines.
- If something is missing, use null or [].

Candidate profile:
{profile_text}

Job content:
{job_text}
"""


MARKET_REQUIREMENT_EXTRACTION_PROMPT = """
You are an AI career-market analyst.

Extract role expectations from the following job-market content.

Return ONLY valid JSON with this exact schema:
{{
  "role": "string",
  "skills": ["string", "..."],
  "tools_frameworks": ["string", "..."],
  "certifications": ["string", "..."],
  "experience_expectations": ["string", "..."],
  "keywords": ["string", "..."],
  "summary": "short summary"
}}

Rules:
- Deduplicate concise items.
- Only include items strongly supported by the content.
- summary should be 2-4 lines.
- If a section is missing, use [] or an empty string.

Target role:
{target_role}

Target package:
{package_text}

Market content:
{market_text}
"""


LEARNING_RESOURCE_EXTRACTION_PROMPT = """
You are an AI learning-resource extractor.

Extract useful learning resources for a target career path.

Return ONLY valid JSON with this exact schema:
{{
  "title": "string",
  "resource_type": "github|documentation|tutorial|roadmap|article|course|other",
  "skills_covered": ["string", "..."],
  "summary": "short summary",
  "difficulty": "beginner|intermediate|advanced|mixed|unknown"
}}

Rules:
- Do not invent fields.
- Keep skills concise.
- summary should be 1-3 lines.
- Use 'other' if the resource type is unclear.

Target role:
{target_role}

Resource content:
{resource_text}
"""


RESUME_ANALYSIS_PROMPT = """
You are an expert resume reviewer, ATS analyst, and career advisor.

You are given:
1. The user's extracted resume/profile
2. Job-market expectations for the target role
3. Open-source learning resources

Return ONLY valid JSON with this exact schema:
{{
  "fit_analysis": {{
    "resume_strength_score": number,
    "role_readiness_score": number,
    "package_readiness_score": number,
    "ats_score": number,
    "strengths": ["string", "..."],
    "overall_summary": "string"
  }},
  "gap_report": {{
    "missing_skills": ["string", "..."],
    "missing_tools_frameworks": ["string", "..."],
    "missing_certifications": ["string", "..."],
    "weak_projects": ["string", "..."],
    "weak_keywords": ["string", "..."],
    "experience_gap": "string"
  }},
  "resume_modifications": {{
    "summary_suggestions": ["string", "..."],
    "project_rewrite_suggestions": ["string", "..."],
    "skills_section_improvements": ["string", "..."],
    "missing_sections": ["string", "..."],
    "ats_keyword_improvements": ["string", "..."]
  }},
  "career_growth_suggestions": {{
    "skills_to_learn_next": ["string", "..."],
    "certifications_to_consider": ["string", "..."],
    "projects_to_build": ["string", "..."],
    "interview_topics": ["string", "..."]
  }},
  "final_recommendation": "string"
}}

Rules:
- Scores must be between 0 and 100.
- Be practical and specific.
- Base conclusions on the provided data only.
- Keep items concise and useful.
- If unsure, return the safest grounded answer.

Extracted resume/profile:
{profile_text}

Market requirements:
{market_text}

Learning resources summary:
{resource_text}
"""
JOB_DETAIL_EXTRACTION_PROMPT = """
You are an AI job description extractor.

Extract the full structured details of a specific job posting.

Return ONLY valid JSON with this exact schema:
{{
  "title": "string",
  "company": "string",
  "location": "string or null",
  "salary": "string or null",
  "experience_text": "string or null",
  "required_skills": ["string", "..."],
  "tools_frameworks": ["string", "..."],
  "certifications": ["string", "..."],
  "keywords": ["string", "..."],
  "summary": "string",
  "description": "string",
  "responsibilities": ["string", "..."],
  "apply_url": "string or null"
}}

Rules:
- Use concise deduplicated lists.
- Extract only what is supported by the job text.
- If something is not available, use null or [].
- summary should be 2-4 lines.
- description should be a clean usable version of the JD.

Job content:
{job_text}
"""


JOB_RESUME_MATCH_PROMPT = """
You are an expert ATS evaluator, recruiter-style screener, and resume-job matcher.

You are given:
1. The user's extracted resume/profile
2. A specific selected job description

Return ONLY valid JSON with this exact schema:
{{
  "job_fit_summary": {{
    "overall_match_score": number,
    "skills_match_score": number,
    "ats_match_score": number,
    "experience_match_score": number,
    "project_relevance_score": number,
    "certification_match_score": number,
    "summary": "string"
  }},
  "strengths": ["string", "..."],
  "gaps": {{
    "missing_skills": ["string", "..."],
    "missing_tools_frameworks": ["string", "..."],
    "missing_keywords": ["string", "..."],
    "missing_certifications": ["string", "..."],
    "experience_gaps": ["string", "..."],
    "project_alignment_issues": ["string", "..."]
  }},
  "resume_improvements": {{
    "summary_improvements": ["string", "..."],
    "project_bullet_improvements": ["string", "..."],
    "keyword_improvements": ["string", "..."],
    "skills_section_improvements": ["string", "..."]
  }},
  "final_recommendation": "Strong Match - Apply now | Moderate Match - Improve before applying | Low Match - Not a strong fit yet"
}}

Rules:
- All scores must be between 0 and 100.
- Be practical and job-specific.
- Only use evidence from the provided resume/profile and job description.
- Do not invent experience.
- Suggestions must be tailored to this exact job.

Resume/profile:
{profile_text}

Selected job details:
{job_text}
"""


AUTO_APPLY_ASSISTANT_PROMPT = """
You are a senior career coach, resume strategist, recruiter, and job application assistant.

Generate a detailed, job-specific application preparation package.

IMPORTANT:
- You only generate the application content fields.
- Do not generate profile, selected_job, apply_url, or safety_note.
- Do not claim the application was submitted.
- The user must review and submit manually.

Quality rules:
- Make every response specific to the selected job, company, and role.
- Do not give generic advice.
- Use job description keywords naturally.
- Do not invent experience, certifications, employment history, salary, notice period, or personal details.
- If salary, notice period, relocation, or work authorization is not provided, answer carefully and say it can be discussed.
- If the resume does not prove something, say it as a suggestion, not as a fact.
- Cover letter must be polished, professional, and ready to use.
- Recruiter message must be short, direct, and suitable for LinkedIn/email.
- Referral message must be polite, concise, and human.
- Application answers must cover common job application questions.
- Resume improvement notes must be actionable and specific.
- Risk warnings must mention weak fit areas, missing skills, or missing proof from resume.
- Score must be between 0 and 100.

Generate:
- 6 resume improvement notes
- 8 application answers
- 1 cover letter with 4 paragraphs
- 1 recruiter message
- 1 referral message
- 8 apply checklist items
- 4 risk warnings

Application answer questions should include:
- Why are you interested in this role?
- Why should we hire you?
- What relevant experience do you have?
- What are your strongest skills for this role?
- Are you willing to relocate?
- What is your notice period?
- What are your salary expectations?
- Do you have any projects relevant to this role?

Candidate profile:
{profile_text}

Selected job:
{job_text}

User preferences:
{preferences_text}
"""