function JobMatchScoreCard({ summary }) {
  return (
    <div className="analysis-card">
      <h3>Job Fit Summary</h3>

      <div className="score-grid">
        <div className="score-box">
          <span>Overall Match</span>
          <strong>{summary.overall_match_score}</strong>
        </div>

        <div className="score-box">
          <span>Skills Match</span>
          <strong>{summary.skills_match_score}</strong>
        </div>

        <div className="score-box">
          <span>ATS Match</span>
          <strong>{summary.ats_match_score}</strong>
        </div>

        <div className="score-box">
          <span>Experience Match</span>
          <strong>{summary.experience_match_score}</strong>
        </div>

        <div className="score-box">
          <span>Project Relevance</span>
          <strong>{summary.project_relevance_score}</strong>
        </div>

        <div className="score-box">
          <span>Certification Match</span>
          <strong>{summary.certification_match_score}</strong>
        </div>
      </div>

      <div className="analysis-block">
        <h4>Summary</h4>
        <p>{summary.summary || "No summary available."}</p>
      </div>
    </div>
  );
}

export default JobMatchScoreCard;
