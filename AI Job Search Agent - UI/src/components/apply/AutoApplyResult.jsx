import { useState } from "react";

function AutoApplyResult({ result }) {
  const [copiedKey, setCopiedKey] = useState("");

  const copyText = async (key, text) => {
    try {
      await navigator.clipboard.writeText(text || "");
      setCopiedKey(key);

      setTimeout(() => {
        setCopiedKey("");
      }, 1800);
    } catch {
      alert("Copy failed. Please copy manually.");
    }
  };

  const copyButtonText = (key) => {
    return copiedKey === key ? "Copied ✓" : "Copy";
  };

  return (
    <div className="analysis-dashboard">
      <div className="analysis-overview-card">
        <h2>Application package ready</h2>

        <div className="score-grid">
          <div className="score-box">
            <span>Apply Readiness</span>
            <strong>{result.apply_readiness_score}</strong>
          </div>
        </div>

        <p className="analysis-final-recommendation">
          {result.final_recommendation}
        </p>

        <p className="muted">{result.safety_note}</p>

        {result.apply_url && (
          <div className="job-actions">
            <a
              className="primary-btn link-btn"
              href={result.apply_url}
              target="_blank"
              rel="noreferrer"
            >
              Open apply link
            </a>
          </div>
        )}
      </div>

      <div className="analysis-card">
        <h3>Resume improvement notes</h3>
        {result.resume_improvement_notes?.length ? (
          <ul className="bullet-list">
            {result.resume_improvement_notes.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No resume improvement notes generated.</p>
        )}
      </div>

      <div className="analysis-card">
        <div className="copy-header">
          <h3>Cover letter</h3>
          <button
            className={
              copiedKey === "cover_letter" ? "copied-btn" : "secondary-btn"
            }
            onClick={() => copyText("cover_letter", result.cover_letter)}
          >
            {copyButtonText("cover_letter")}
          </button>
        </div>
        <p className="long-text">{result.cover_letter}</p>
      </div>

      <div className="analysis-card">
        <div className="copy-header">
          <h3>Recruiter message</h3>
          <button
            className={
              copiedKey === "recruiter_message" ? "copied-btn" : "secondary-btn"
            }
            onClick={() =>
              copyText("recruiter_message", result.recruiter_message)
            }
          >
            {copyButtonText("recruiter_message")}
          </button>
        </div>
        <p className="long-text">{result.recruiter_message}</p>
      </div>

      <div className="analysis-card">
        <div className="copy-header">
          <h3>Referral message</h3>
          <button
            className={
              copiedKey === "referral_message" ? "copied-btn" : "secondary-btn"
            }
            onClick={() =>
              copyText("referral_message", result.referral_message)
            }
          >
            {copyButtonText("referral_message")}
          </button>
        </div>
        <p className="long-text">{result.referral_message}</p>
      </div>

      <div className="analysis-card">
        <h3>Application form answers</h3>

        {result.application_answers?.length ? (
          result.application_answers.map((item, index) => {
            const key = `answer_${index}`;

            return (
              <div className="qa-card" key={`${item.question}-${index}`}>
                <div className="copy-header">
                  <strong>{item.question}</strong>
                  <button
                    className={
                      copiedKey === key ? "copied-btn" : "secondary-btn"
                    }
                    onClick={() => copyText(key, item.answer)}
                  >
                    {copiedKey === key ? "Copied ✓" : "Copy answer"}
                  </button>
                </div>
                <p>{item.answer}</p>
              </div>
            );
          })
        ) : (
          <p className="muted">No application answers generated.</p>
        )}
      </div>

      <div className="analysis-card">
        <h3>Apply checklist</h3>
        {result.apply_checklist?.length ? (
          <ul className="bullet-list">
            {result.apply_checklist.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No checklist generated.</p>
        )}
      </div>

      <div className="analysis-card">
        <h3>Risk warnings</h3>
        {result.risk_warnings?.length ? (
          <ul className="bullet-list">
            {result.risk_warnings.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">No risk warnings generated.</p>
        )}
      </div>
    </div>
  );
}

export default AutoApplyResult;
