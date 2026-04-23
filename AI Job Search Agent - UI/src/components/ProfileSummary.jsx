function renderList(items) {
  if (!items || items.length === 0) {
    return "Not provided";
  }
  return items.join(", ");
}

function ProfileSummary({ profile, totalFound }) {
  return (
    <aside className="summary-card">
      <h3>Profile Summary</h3>
      <div className="summary-item">
        <span>Desired Role</span>
        <strong>{profile.desired_role || "Not provided"}</strong>
      </div>
      <div className="summary-item">
        <span>Experience</span>
        <strong>
          {profile.years_experience !== null &&
          profile.years_experience !== undefined
            ? `${profile.years_experience} years`
            : "Not provided"}
        </strong>
      </div>
      <div className="summary-item">
        <span>Location</span>
        <strong>{profile.location || "Not provided"}</strong>
      </div>
      <div className="summary-item">
        <span>Skills</span>
        <strong>{renderList(profile.skills)}</strong>
      </div>
      <div className="summary-item">
        <span>Certifications</span>
        <strong>{renderList(profile.certifications)}</strong>
      </div>
      <div className="summary-item">
        <span>Preferred Companies</span>
        <strong>{renderList(profile.companies)}</strong>
      </div>
      <div className="summary-item">
        <span>Expected Package</span>
        <strong>
          {profile.package_min_lpa || profile.package_max_lpa
            ? `${profile.package_min_lpa || "-"} - ${profile.package_max_lpa || "-"} LPA`
            : "Not provided"}
        </strong>
      </div>
      <div className="summary-item">
        <span>Total Jobs Found</span>
        <strong>{totalFound}</strong>
      </div>
    </aside>
  );
}

export default ProfileSummary;
