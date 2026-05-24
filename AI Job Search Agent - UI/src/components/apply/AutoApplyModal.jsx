import { useState } from "react";
import AutoApplyResult from "./AutoApplyResult";
import { prepareApplicationPackage } from "../../api/client";

function AutoApplyModal({ job, onClose }) {
  const [file, setFile] = useState(null);
  const [coverLetterTone, setCoverLetterTone] = useState("professional");
  const [noticePeriod, setNoticePeriod] = useState("");
  const [expectedSalary, setExpectedSalary] = useState("");
  const [currentLocation, setCurrentLocation] = useState("");
  const [willingToRelocate, setWillingToRelocate] = useState("");
  const [workAuthorization, setWorkAuthorization] = useState("");
  const [portfolioUrl, setPortfolioUrl] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please upload your resume.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await prepareApplicationPackage(file, job, {
        coverLetterTone,
        noticePeriod,
        expectedSalary,
        currentLocation,
        willingToRelocate,
        workAuthorization,
        portfolioUrl,
        githubUrl,
        linkedinUrl,
      });

      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to prepare your application kit.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <div>
            <span className="eyebrow">Application kit</span>
            <h2>Prepare your job application</h2>
            <p className="modal-subtitle">
              Generate a tailored cover letter, recruiter note, referral
              request, application answers, and final application checklist.
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
          <div className="job-meta">
            <span>{job.location || "Location not specified"}</span>
            <span>{job.salary || "Salary not specified"}</span>
          </div>
          <p className="job-summary">
            {job.summary || "No summary available."}
          </p>
        </div>

        {!result ? (
          <form className="form-grid" onSubmit={handleSubmit}>
            <div className="form-group form-group-full">
              <label>Resume file</label>
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </div>

            <div className="form-group">
              <label>Cover letter tone</label>
              <input
                value={coverLetterTone}
                onChange={(e) => setCoverLetterTone(e.target.value)}
                placeholder="professional, confident, concise"
              />
            </div>

            <div className="form-group">
              <label>Notice period</label>
              <input
                value={noticePeriod}
                onChange={(e) => setNoticePeriod(e.target.value)}
                placeholder="Immediate, 30 days, 60 days"
              />
            </div>

            <div className="form-group">
              <label>Expected salary</label>
              <input
                value={expectedSalary}
                onChange={(e) => setExpectedSalary(e.target.value)}
                placeholder="10 LPA, Negotiable"
              />
            </div>

            <div className="form-group">
              <label>Current location</label>
              <input
                value={currentLocation}
                onChange={(e) => setCurrentLocation(e.target.value)}
                placeholder="Hyderabad"
              />
            </div>

            <div className="form-group">
              <label>Willing to relocate</label>
              <input
                value={willingToRelocate}
                onChange={(e) => setWillingToRelocate(e.target.value)}
                placeholder="Yes / No / Depends"
              />
            </div>

            <div className="form-group">
              <label>Work authorization</label>
              <input
                value={workAuthorization}
                onChange={(e) => setWorkAuthorization(e.target.value)}
                placeholder="Authorized to work in India"
              />
            </div>

            <div className="form-group">
              <label>Portfolio URL</label>
              <input
                value={portfolioUrl}
                onChange={(e) => setPortfolioUrl(e.target.value)}
                placeholder="https://portfolio.com"
              />
            </div>

            <div className="form-group">
              <label>GitHub URL</label>
              <input
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="https://github.com/username"
              />
            </div>

            <div className="form-group form-group-full">
              <label>LinkedIn URL</label>
              <input
                value={linkedinUrl}
                onChange={(e) => setLinkedinUrl(e.target.value)}
                placeholder="https://linkedin.com/in/username"
              />
            </div>

            {error && <div className="error-box form-group-full">{error}</div>}

            <div className="form-actions form-group-full">
              <button type="submit" className="primary-btn" disabled={loading}>
                {loading
                  ? "Building your application kit..."
                  : "Build application kit"}
              </button>
            </div>
          </form>
        ) : (
          <AutoApplyResult result={result} />
        )}
      </div>
    </div>
  );
}

export default AutoApplyModal;
