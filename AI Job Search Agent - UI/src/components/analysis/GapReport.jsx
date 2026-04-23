function GapReport({ gap }) {
  return (
    <div className="analysis-card">
      <h3>Gap Report</h3>

      <div className="analysis-block">
        <h4>Missing Skills</h4>
        {gap.missing_skills?.length ? (
          <div className="tag-list">
            {gap.missing_skills.map((item, index) => (
              <span key={`${item}-${index}`} className="tag missing">
                {item}
              </span>
            ))}
          </div>
        ) : (
          <p className="muted">No major skill gaps detected.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Missing Tools / Frameworks</h4>
        {gap.missing_tools_frameworks?.length ? (
          <div className="tag-list">
            {gap.missing_tools_frameworks.map((item, index) => (
              <span key={`${item}-${index}`} className="tag missing">
                {item}
              </span>
            ))}
          </div>
        ) : (
          <p className="muted">No major tool gaps detected.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Missing Certifications</h4>
        {gap.missing_certifications?.length ? (
          <ul className="bullet-list">
            {gap.missing_certifications.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No major certification gap detected.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Weak Projects</h4>
        {gap.weak_projects?.length ? (
          <ul className="bullet-list">
            {gap.weak_projects.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No weak project notes available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Weak Keywords</h4>
        {gap.weak_keywords?.length ? (
          <div className="tag-list">
            {gap.weak_keywords.map((item, index) => (
              <span key={`${item}-${index}`} className="tag">
                {item}
              </span>
            ))}
          </div>
        ) : (
          <p className="muted">No keyword issues found.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Experience Gap</h4>
        <p>{gap.experience_gap || "No experience gap noted."}</p>
      </div>
    </div>
  );
}

export default GapReport;
