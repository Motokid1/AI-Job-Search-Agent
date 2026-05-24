import { useState } from "react";
import {
  cancelAutoApplySession,
  resumeAutoApplySession,
  startAutoApplySession,
} from "../../api/client";

function AutoApplyRuntimeModal({ job, onClose }) {
  const [file, setFile] = useState(null);
  const [candidate, setCandidate] = useState({
    full_name: "",
    email: "",
    phone: "",
    current_location: "",
    linkedin_url: "",
    github_url: "",
    portfolio_url: "",
    expected_salary: "",
    notice_period: "",
    willing_to_relocate: "",
    work_authorization: "",
    cover_letter: "",
  });

  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const updateCandidate = (key, value) => {
    setCandidate((prev) => ({ ...prev, [key]: value }));
  };

  const startSession = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Please upload resume.");
      return;
    }

    try {
      setLoading(true);
      setMessage("Starting browser automation...");
      const response = await startAutoApplySession(file, job, candidate);
      setSession(response);
      setMessage(response.message);
    } catch (err) {
      setMessage(err.message || "Failed to start auto apply.");
    } finally {
      setLoading(false);
    }
  };

  const handleDecision = async (decision) => {
    if (!session?.session_id) return;

    try {
      setLoading(true);
      const response = await resumeAutoApplySession(
        session.session_id,
        decision,
      );
      setSession(response);
      setMessage(response.message);
    } catch (err) {
      setMessage(err.message || "Failed to resume session.");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async () => {
    if (!session?.session_id) {
      onClose();
      return;
    }

    const response = await cancelAutoApplySession(session.session_id);
    setSession(response);
    setMessage(response.message);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card compact-modal">
        <div className="modal-header">
          <div>
            <span className="eyebrow">Human-approved auto apply</span>
            <h2>Auto-fill application form</h2>
            <p className="modal-subtitle">
              The browser will fill the form and pause before final submission.
            </p>
          </div>

          <button className="modal-close-btn" onClick={onClose}>
            Close
          </button>
        </div>

        <div className="selected-job-card">
          <p className="job-company">
            {job.company || "Company not specified"}
          </p>
          <h3>{job.title}</h3>
          <p className="job-summary">{job.apply_url || job.source_url}</p>
        </div>

        {!session && (
          <form className="form-grid" onSubmit={startSession}>
            <div className="form-group form-group-full">
              <label>Resume file</label>
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </div>

            {Object.keys(candidate).map((key) => (
              <div
                className={
                  key === "cover_letter"
                    ? "form-group form-group-full"
                    : "form-group"
                }
                key={key}
              >
                <label>{key.replaceAll("_", " ")}</label>
                <input
                  value={candidate[key]}
                  onChange={(e) => updateCandidate(key, e.target.value)}
                />
              </div>
            ))}

            <div className="form-actions form-group-full">
              <button type="submit" className="primary-btn" disabled={loading}>
                {loading ? "Starting..." : "Start auto apply"}
              </button>
            </div>
          </form>
        )}

        {session && (
          <div className="analysis-dashboard">
            <div className="analysis-overview-card">
              <h3>Status</h3>
              <p>
                <strong>{session.status}</strong>
              </p>
              <p>{message || session.message}</p>

              {session.browser_url && (
                <p>
                  Browser URL: <strong>{session.browser_url}</strong>
                </p>
              )}
            </div>

            {session.requires_user_action && (
              <div className="analysis-card">
                <h3>Human approval required</h3>
                <p>
                  Please review the opened browser window before submitting.
                </p>

                <div className="job-actions">
                  <button
                    className="success-btn"
                    onClick={() => handleDecision("submit")}
                    disabled={loading}
                  >
                    Submit application
                  </button>

                  <button
                    className="secondary-btn"
                    onClick={() => handleDecision("manual_review")}
                    disabled={loading}
                  >
                    Continue manual review
                  </button>

                  <button
                    className="danger-btn"
                    onClick={() => handleDecision("cancel")}
                    disabled={loading}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {session.detected_fields?.length > 0 && (
              <div className="analysis-card">
                <h3>Detected fields</h3>
                <ul className="bullet-list">
                  {session.detected_fields.slice(0, 10).map((field, index) => (
                    <li key={index}>
                      {field.tag} / {field.type || "text"} /{" "}
                      {field.name || field.placeholder || field.id || "unknown"}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {session && (
          <div className="form-actions">
            <button className="secondary-btn" onClick={handleCancel}>
              End session
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default AutoApplyRuntimeModal;
