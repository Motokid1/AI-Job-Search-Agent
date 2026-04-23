function LearningResources({ resources }) {
  return (
    <div className="analysis-card">
      <h3>Learning Resources</h3>

      {!resources.length ? (
        <p className="muted">No learning resources available.</p>
      ) : (
        <div className="resource-list">
          {resources.map((resource, index) => (
            <div key={`${resource.url}-${index}`} className="resource-card">
              <div className="resource-top">
                <div>
                  <h4>{resource.title}</h4>
                  <p className="resource-type">
                    {resource.resource_type} • {resource.difficulty}
                  </p>
                </div>
              </div>

              <p>{resource.summary}</p>

              <div className="tag-list">
                {resource.skills_covered?.map((skill, idx) => (
                  <span key={`${skill}-${idx}`} className="tag">
                    {skill}
                  </span>
                ))}
              </div>

              <div className="job-actions">
                <a
                  className="primary-btn link-btn"
                  href={resource.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open Resource
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default LearningResources;
