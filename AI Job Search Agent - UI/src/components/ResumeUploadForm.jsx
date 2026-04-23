import { useState } from "react";
import { searchJobsResume } from "../api/client";

function ResumeUploadForm({
  onSearchStart,
  onSearchSuccess,
  onSearchError,
  onReset,
}) {
  const [file, setFile] = useState(null);
  const [desiredRole, setDesiredRole] = useState("");
  const [location, setLocation] = useState("");
  const [packageMinLpa, setPackageMinLpa] = useState("");
  const [packageMaxLpa, setPackageMaxLpa] = useState("");
  const [companies, setCompanies] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      onSearchError("Please upload a resume file.");
      return;
    }

    try {
      onReset();
      onSearchStart();

      const data = await searchJobsResume({
        file,
        desiredRole,
        location,
        packageMinLpa,
        packageMaxLpa,
        companies,
      });

      onSearchSuccess(data);
    } catch (error) {
      onSearchError(error.message);
    }
  };

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <div className="form-group form-group-full">
        <label>Upload Resume (PDF/DOCX)</label>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      <div className="form-group">
        <label>Desired Role</label>
        <input
          type="text"
          placeholder="Java Backend Developer"
          value={desiredRole}
          onChange={(e) => setDesiredRole(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Preferred Location</label>
        <input
          type="text"
          placeholder="Hyderabad"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Minimum Package (LPA)</label>
        <input
          type="number"
          step="0.1"
          placeholder="8"
          value={packageMinLpa}
          onChange={(e) => setPackageMinLpa(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Maximum Package (LPA)</label>
        <input
          type="number"
          step="0.1"
          placeholder="12"
          value={packageMaxLpa}
          onChange={(e) => setPackageMaxLpa(e.target.value)}
        />
      </div>

      <div className="form-group form-group-full">
        <label>Preferred Companies (comma separated)</label>
        <input
          type="text"
          placeholder="TCS, Infosys, Deloitte"
          value={companies}
          onChange={(e) => setCompanies(e.target.value)}
        />
      </div>

      <div className="form-actions form-group-full">
        <button type="submit" className="primary-btn">
          Search Jobs
        </button>
      </div>
    </form>
  );
}

export default ResumeUploadForm;
