import JobMatchScoreCard from "./JobMatchScoreCard";

function JobMatchResult({ result }) {
  const {
    selected_job,
    job_fit_summary,
    strengths,
    gaps,
    resume_improvements,
    final_recommendation,
  } = result;

  return (
    <div className="analysis-dashboard">
      <div className="analysis-overview-card">
        <h2>Selected Job Details</h2>
        <p>
          <strong>Title:</strong> {selected_job.title}
        </p>
        <p>
          <strong>Company:</strong> {selected_job.company}
        </p>
        <p>
          <strong>Location:</strong> {selected_job.location || "Not specified"}
        </p>
        <p>
          <strong>Salary:</strong> {selected_job.salary || "Not specified"}
        </p>
        <p>
          <strong>Experience:</strong>{" "}
          {selected_job.experience_text || "Not specified"}
        </p>
        <p className="analysis-final-recommendation">{final_recommendation}</p>
      </div>

      <JobMatchScoreCard summary={job_fit_summary} />

      <div className="analysis-card">
        <h3>Strengths</h3>
        {strengths?.length ? (
          <ul className="bullet-list">
            {strengths.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No strengths available.</p>
        )}
      </div>

      <div className="analysis-card">
        <h3>Gaps</h3>

        <div className="analysis-block">
          <h4>Missing Skills</h4>
          {gaps.missing_skills?.length ? (
            <div className="tag-list">
              {gaps.missing_skills.map((item, index) => (
                <span key={`${item}-${index}`} className="tag missing">
                  {item}
                </span>
              ))}
            </div>
          ) : (
            <p className="muted">No missing skills detected.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Missing Tools / Frameworks</h4>
          {gaps.missing_tools_frameworks?.length ? (
            <div className="tag-list">
              {gaps.missing_tools_frameworks.map((item, index) => (
                <span key={`${item}-${index}`} className="tag missing">
                  {item}
                </span>
              ))}
            </div>
          ) : (
            <p className="muted">No missing tools detected.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Missing Keywords</h4>
          {gaps.missing_keywords?.length ? (
            <div className="tag-list">
              {gaps.missing_keywords.map((item, index) => (
                <span key={`${item}-${index}`} className="tag">
                  {item}
                </span>
              ))}
            </div>
          ) : (
            <p className="muted">No missing keywords detected.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Missing Certifications</h4>
          {gaps.missing_certifications?.length ? (
            <ul className="bullet-list">
              {gaps.missing_certifications.map((item, index) => (
                <li key={`${item}-${index}`}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No certification gaps detected.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Experience Gaps</h4>
          {gaps.experience_gaps?.length ? (
            <ul className="bullet-list">
              {gaps.experience_gaps.map((item, index) => (
                <li key={`${item}-${index}`}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No major experience gaps detected.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Project Alignment Issues</h4>
          {gaps.project_alignment_issues?.length ? (
            <ul className="bullet-list">
              {gaps.project_alignment_issues.map((item, index) => (
                <li key={`${item}-${index}`}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No project alignment issues found.</p>
          )}
        </div>
      </div>

      <div className="analysis-card">
        <h3>Resume Improvements for This Job</h3>

        <div className="analysis-block">
          <h4>Summary Improvements</h4>
          {resume_improvements.summary_improvements?.length ? (
            <ul className="bullet-list">
              {resume_improvements.summary_improvements.map((item, index) => (
                <li key={`${item}-${index}`}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No summary improvements available.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Project Bullet Improvements</h4>
          {resume_improvements.project_bullet_improvements?.length ? (
            <ul className="bullet-list">
              {resume_improvements.project_bullet_improvements.map(
                (item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ),
              )}
            </ul>
          ) : (
            <p className="muted">No project bullet improvements available.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Keyword Improvements</h4>
          {resume_improvements.keyword_improvements?.length ? (
            <div className="tag-list">
              {resume_improvements.keyword_improvements.map((item, index) => (
                <span key={`${item}-${index}`} className="tag">
                  {item}
                </span>
              ))}
            </div>
          ) : (
            <p className="muted">No keyword improvements available.</p>
          )}
        </div>

        <div className="analysis-block">
          <h4>Skills Section Improvements</h4>
          {resume_improvements.skills_section_improvements?.length ? (
            <ul className="bullet-list">
              {resume_improvements.skills_section_improvements.map(
                (item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ),
              )}
            </ul>
          ) : (
            <p className="muted">No skill-section improvements available.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default JobMatchResult;
