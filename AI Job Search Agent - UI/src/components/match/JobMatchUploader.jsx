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
      onSuccess(data);
    } catch (err) {
      setError(err.message || "Job-specific analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="job-match-upload-section">
      <h3>Upload your resume</h3>
      <p className="muted">
        The system will fetch the job description, compare it with your resume,
        and return a role-specific fit score.
      </p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-group form-group-full">
          <label>Resume file</label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div className="form-actions form-group-full">
          <button type="submit" className="primary-btn" disabled={loading}>
            {loading ? "Analyzing..." : "Generate fit report"}
          </button>
        </div>
      </form>

      {error && <div className="error-box">{error}</div>}
    </div>
  );
}

export default JobMatchUploader;
