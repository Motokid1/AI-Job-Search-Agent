function CareerSuggestions({ data }) {
  return (
    <div className="analysis-card">
      <h3>Career Growth Suggestions</h3>

      <div className="analysis-block">
        <h4>Skills to Learn Next</h4>
        {data.skills_to_learn_next?.length ? (
          <div className="tag-list">
            {data.skills_to_learn_next.map((item, index) => (
              <span key={`${item}-${index}`} className="tag">
                {item}
              </span>
            ))}
          </div>
        ) : (
          <p className="muted">No learning suggestions available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Certifications to Consider</h4>
        {data.certifications_to_consider?.length ? (
          <ul className="bullet-list">
            {data.certifications_to_consider.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No certification suggestions available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Projects to Build</h4>
        {data.projects_to_build?.length ? (
          <ul className="bullet-list">
            {data.projects_to_build.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No project suggestions available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Interview Topics</h4>
        {data.interview_topics?.length ? (
          <ul className="bullet-list">
            {data.interview_topics.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No interview topics available.</p>
        )}
      </div>
    </div>
  );
}

export default CareerSuggestions;
