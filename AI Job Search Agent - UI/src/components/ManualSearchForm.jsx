import { useState } from "react";
import { searchJobsManual } from "../api/client";

function ManualSearchForm({
  onSearchStart,
  onSearchSuccess,
  onSearchError,
  onReset,
}) {
  const [desiredRole, setDesiredRole] = useState("");
  const [skills, setSkills] = useState("");
  const [yearsExperience, setYearsExperience] = useState("");
  const [certifications, setCertifications] = useState("");
  const [location, setLocation] = useState("");
  const [packageMinLpa, setPackageMinLpa] = useState("");
  const [packageMaxLpa, setPackageMaxLpa] = useState("");
  const [companies, setCompanies] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      onReset();
      onSearchStart();

      const payload = {
        desired_role: desiredRole || null,
        skills: skills
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        years_experience: yearsExperience ? Number(yearsExperience) : null,
        certifications: certifications
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        location: location || null,
        package_min_lpa: packageMinLpa ? Number(packageMinLpa) : null,
        package_max_lpa: packageMaxLpa ? Number(packageMaxLpa) : null,
        companies: companies
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
      };

      const data = await searchJobsManual(payload);
      onSearchSuccess(data);
    } catch (error) {
      onSearchError(error.message);
    }
  };

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
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
        <label>Years of Experience</label>
        <input
          type="number"
          step="0.1"
          placeholder="2"
          value={yearsExperience}
          onChange={(e) => setYearsExperience(e.target.value)}
        />
      </div>

      <div className="form-group form-group-full">
        <label>Skills (comma separated)</label>
        <input
          type="text"
          placeholder="Java, Spring Boot, REST API, MySQL, AWS"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
      </div>

      <div className="form-group form-group-full">
        <label>Certifications (comma separated, optional)</label>
        <input
          type="text"
          placeholder="AWS Cloud Practitioner, RHCSA"
          value={certifications}
          onChange={(e) => setCertifications(e.target.value)}
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
          placeholder="TCS, Infosys"
          value={companies}
          onChange={(e) => setCompanies(e.target.value)}
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

      <div className="form-actions form-group-full">
        <button type="submit" className="primary-btn">
          Search Jobs
        </button>
      </div>
    </form>
  );
}

export default ManualSearchForm;
