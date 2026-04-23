import { useState } from "react";
import { matchResumeForJob } from "../../api/client";

function JobMatchUploader({ job, onSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please upload your resume.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await matchResumeForJob(file, job);
      console.log("JOB MATCH RESPONSE:", data);
      onSuccess(data);
    } catch (err) {
      setError(err.message || "Job-specific analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="job-match-upload-section">
      <h3>Upload Resume for This Job</h3>
      <p className="muted">
        We will fetch the full JD, compare it with your resume, and generate a
        job-specific fit report.
      </p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-group form-group-full">
          <label>Resume (PDF/DOCX)</label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div className="form-actions form-group-full">
          <button type="submit" className="primary-btn" disabled={loading}>
            {loading ? "Analyzing..." : "Match Resume for This Job"}
          </button>
        </div>
      </form>

      {error && <div className="error-box">{error}</div>}
    </div>
  );
}

export default JobMatchUploader;
