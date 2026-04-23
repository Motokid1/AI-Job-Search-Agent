function ResumeSuggestions({ data }) {
  return (
    <div className="analysis-card">
      <h3>Resume Improvement Suggestions</h3>

      <div className="analysis-block">
        <h4>Summary Suggestions</h4>
        {data.summary_suggestions?.length ? (
          <ul className="bullet-list">
            {data.summary_suggestions.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No summary suggestions available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Project Rewrite Suggestions</h4>
        {data.project_rewrite_suggestions?.length ? (
          <ul className="bullet-list">
            {data.project_rewrite_suggestions.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No project rewrite suggestions available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Skills Section Improvements</h4>
        {data.skills_section_improvements?.length ? (
          <ul className="bullet-list">
            {data.skills_section_improvements.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No skills-section changes suggested.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Missing Sections</h4>
        {data.missing_sections?.length ? (
          <ul className="bullet-list">
            {data.missing_sections.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No missing sections detected.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>ATS Keyword Improvements</h4>
        {data.ats_keyword_improvements?.length ? (
          <div className="tag-list">
            {data.ats_keyword_improvements.map((item, index) => (
              <span key={`${item}-${index}`} className="tag">
                {item}
              </span>
            ))}
          </div>
        ) : (
          <p className="muted">No ATS keyword improvements suggested.</p>
        )}
      </div>
    </div>
  );
}

export default ResumeSuggestions;
