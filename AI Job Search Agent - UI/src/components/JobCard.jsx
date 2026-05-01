function JobCard({ job, onAnalyzeJob }) {
  return (
    <article className="job-card">
      <div className="job-card-top">
        <div>
          <p className="job-company">
            {job.company || "Company not specified"}
          </p>
          <h3>{job.title}</h3>
        </div>
        <div className="score-badge">{job.match_score}%</div>
      </div>

      <div className="job-meta">
        <span>{job.location || "Location not specified"}</span>
        <span>{job.salary || "Salary not specified"}</span>
        <span>{job.experience_text || "Experience not specified"}</span>
      </div>

      <p className="job-summary">{job.summary || "No summary available."}</p>

      <div className="tag-block">
        <h4>Required skills</h4>
        <div className="tag-list">
          {job.required_skills?.length ? (
            job.required_skills.map((skill, index) => (
              <span key={`${skill}-${index}`} className="tag">
                {skill}
              </span>
            ))
          ) : (
            <span className="muted">No skills extracted</span>
          )}
        </div>
      </div>

      <div className="tag-block">
        <h4>Why this matches</h4>
        {job.match_reasons?.length ? (
          <ul className="bullet-list">
            {job.match_reasons.map((reason, index) => (
              <li key={`${reason}-${index}`}>{reason}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No match reasons available.</p>
        )}
      </div>

      <div className="job-actions">
        <a
          className="primary-btn link-btn"
          href={job.apply_url || job.source_url}
          target="_blank"
          rel="noreferrer"
        >
          View role
        </a>

        <a
          className="secondary-btn link-btn"
          href={job.source_url}
          target="_blank"
          rel="noreferrer"
        >
          Source
        </a>

        <button
          type="button"
          className="success-btn"
          onClick={() => onAnalyzeJob?.(job)}
        >
          Match my resume
        </button>
      </div>
    </article>
  );
}

export default JobCard;
