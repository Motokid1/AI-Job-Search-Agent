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
            <span className="eyebrow">Job-specific resume match</span>
            <h2>Evaluate your resume for this role</h2>
            <p className="modal-subtitle">
              We will compare your resume against the selected job description
              and generate a fit report.
            </p>
          </div>

          <button className="modal-close-btn" onClick={onClose}>
            Close
          </button>
        </div>

        <div className="selected-job-card">
          <p className="job-company">{job.company}</p>
          <h3>{job.title}</h3>
          <div className="job-meta">
            <span>{job.location || "Location not specified"}</span>
            <span>{job.salary || "Salary not specified"}</span>
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
