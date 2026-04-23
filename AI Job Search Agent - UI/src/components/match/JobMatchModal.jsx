import { useState } from "react";
import JobMatchUploader from "./JobMatchUploader";
import JobMatchResult from "./JobMatchResult";

function JobMatchModal({ job, onClose }) {
  const [result, setResult] = useState(null);

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <div>
            <h2>Job-Specific Resume Match</h2>
            <p className="modal-subtitle">
              Analyze your resume for this exact job posting.
            </p>
          </div>

          <button className="modal-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="selected-job-card">
          <h3>{job.title}</h3>
          <p className="job-company">{job.company}</p>
          <div className="job-meta">
            <span>📍 {job.location || "Location not specified"}</span>
            <span>💰 {job.salary || "Salary not specified"}</span>
          </div>
          <p className="job-summary">
            {job.summary || "No summary available."}
          </p>
        </div>

        {!result ? (
          <JobMatchUploader job={job} onSuccess={setResult} />
        ) : (
          <JobMatchResult result={result} />
        )}
      </div>
    </div>
  );
}

export default JobMatchModal;
