function FitScoreCard({ fit }) {
  return (
    <div className="analysis-card">
      <h3>Fit Analysis</h3>

      <div className="score-grid">
        <div className="score-box">
          <span>Resume Strength</span>
          <strong>{fit.resume_strength_score}</strong>
        </div>

        <div className="score-box">
          <span>Role Readiness</span>
          <strong>{fit.role_readiness_score}</strong>
        </div>

        <div className="score-box">
          <span>Package Readiness</span>
          <strong>{fit.package_readiness_score}</strong>
        </div>

        <div className="score-box">
          <span>ATS Score</span>
          <strong>{fit.ats_score}</strong>
        </div>
      </div>

      <div className="analysis-block">
        <h4>Strengths</h4>
        {fit.strengths?.length ? (
          <ul className="bullet-list">
            {fit.strengths.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No strengths available.</p>
        )}
      </div>

      <div className="analysis-block">
        <h4>Overall Summary</h4>
        <p>{fit.overall_summary || "No summary available."}</p>
      </div>
    </div>
  );
}

export default FitScoreCard;
