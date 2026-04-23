import { useState } from "react";
import { analyzeResume } from "../../api/client";

function AnalysisForm({
  onAnalysisStart,
  onAnalysisSuccess,
  onAnalysisError,
  onReset,
}) {
  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [packageMinLpa, setPackageMinLpa] = useState("");
  const [packageMaxLpa, setPackageMaxLpa] = useState("");
  const [location, setLocation] = useState("");
  const [companies, setCompanies] = useState("");
  const [targetDomain, setTargetDomain] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      onAnalysisError("Please upload a resume file.");
      return;
    }

    if (!targetRole.trim()) {
      onAnalysisError("Please enter a target role.");
      return;
    }

    try {
      onReset();
      onAnalysisStart();

      const data = await analyzeResume({
        file,
        targetRole,
        packageMinLpa,
        packageMaxLpa,
        location,
        companies,
        targetDomain,
      });

      onAnalysisSuccess(data);
    } catch (error) {
      onAnalysisError(error.message);
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
        <label>Target Role</label>
        <input
          type="text"
          placeholder="Java Backend Developer"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Target Domain</label>
        <input
          type="text"
          placeholder="Backend Development"
          value={targetDomain}
          onChange={(e) => setTargetDomain(e.target.value)}
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
        <label>Preferred Companies</label>
        <input
          type="text"
          placeholder="TCS, Infosys, Deloitte"
          value={companies}
          onChange={(e) => setCompanies(e.target.value)}
        />
      </div>

      <div className="form-actions form-group-full">
        <button type="submit" className="primary-btn">
          Analyze Resume
        </button>
      </div>
    </form>
  );
}

export default AnalysisForm;
