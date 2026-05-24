import { useState } from "react";
import { createTrackedApplication } from "../../api/client";

function today() {
  return new Date().toISOString().slice(0, 10);
}

function SaveToTrackerModal({ job, onClose }) {
  const [status, setStatus] = useState("Saved");
  const [appliedDate, setAppliedDate] = useState("");
  const [resumeVersion, setResumeVersion] = useState("");
  const [notes, setNotes] = useState("");
  const [followUpDate, setFollowUpDate] = useState("");
  const [recruiterName, setRecruiterName] = useState("");
  const [recruiterContact, setRecruiterContact] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const handleSave = async (event) => {
    event.preventDefault();

    try {
      setSaving(true);
      setMessage("");

      await createTrackedApplication({
        company: job.company || "Unknown Company",
        role: job.title || "Unknown Role",
        job_url: job.apply_url || job.source_url,
        status,
        applied_date: appliedDate || null,
        resume_version: resumeVersion || null,
        notes: notes || null,
        follow_up_date: followUpDate || null,
        recruiter_name: recruiterName || null,
        recruiter_contact: recruiterContact || null,
      });

      setMessage("Saved to tracker successfully.");
      setTimeout(onClose, 900);
    } catch (err) {
      setMessage(err.message || "Failed to save job.");
    } finally {
      setSaving(false);
    }
  };

  const markApplied = () => {
    setStatus("Applied");
    setAppliedDate(today());
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card compact-modal">
        <div className="modal-header">
          <div>
            <span className="eyebrow">Application tracker</span>
            <h2>Save this job</h2>
            <p className="modal-subtitle">
              Track status, resume version, notes, and follow-up date.
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
        </div>

        <form className="form-grid" onSubmit={handleSave}>
          <div className="form-group">
            <label>Status</label>
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option>Saved</option>
              <option>Applied</option>
              <option>Screening</option>
              <option>Interview</option>
              <option>Final Round</option>
              <option>Offer</option>
              <option>Rejected</option>
            </select>
          </div>

          <div className="form-group">
            <label>Applied date</label>
            <input
              type="date"
              value={appliedDate}
              onChange={(e) => setAppliedDate(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Resume version</label>
            <input
              value={resumeVersion}
              onChange={(e) => setResumeVersion(e.target.value)}
              placeholder="resume_java_backend.pdf"
            />
          </div>

          <div className="form-group">
            <label>Follow-up date</label>
            <input
              type="date"
              value={followUpDate}
              onChange={(e) => setFollowUpDate(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Recruiter name</label>
            <input
              value={recruiterName}
              onChange={(e) => setRecruiterName(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Recruiter contact</label>
            <input
              value={recruiterContact}
              onChange={(e) => setRecruiterContact(e.target.value)}
            />
          </div>

          <div className="form-group form-group-full">
            <label>Notes</label>
            <input
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Applied after resume update..."
            />
          </div>

          {message && (
            <div className="form-group-full success-message">{message}</div>
          )}

          <div className="form-actions form-group-full tracker-actions">
            <button
              type="button"
              className="secondary-btn"
              onClick={markApplied}
            >
              Mark as applied today
            </button>
            <button type="submit" className="primary-btn" disabled={saving}>
              {saving ? "Saving..." : "Save to tracker"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SaveToTrackerModal;
