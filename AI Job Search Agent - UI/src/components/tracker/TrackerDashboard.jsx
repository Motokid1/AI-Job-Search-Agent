import { useEffect, useState } from "react";
import {
  deleteTrackedApplication,
  getTrackedApplications,
  updateTrackedApplication,
} from "../../api/client";

const STATUSES = [
  "All",
  "Saved",
  "Applied",
  "Screening",
  "Interview",
  "Final Round",
  "Offer",
  "Rejected",
];

function TrackerDashboard() {
  const [status, setStatus] = useState("All");
  const [sortBy, setSortBy] = useState("updated_at");
  const [sortOrder, setSortOrder] = useState("desc");
  const [data, setData] = useState({ applications: [], analytics: {} });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadTracker = async () => {
    try {
      setLoading(true);
      setError("");
      const response = await getTrackedApplications({
        status,
        sortBy,
        sortOrder,
      });
      setData(response);
    } catch (err) {
      setError(err.message || "Failed to load tracker.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTracker();
  }, [status, sortBy, sortOrder]);

  const handleStatusChange = async (id, nextStatus) => {
    await updateTrackedApplication(id, { status: nextStatus });
    loadTracker();
  };

  const handleDelete = async (id) => {
    await deleteTrackedApplication(id);
    loadTracker();
  };

  const analytics = data.analytics || {};

  return (
    <section className="tracker-section">
      <div className="section-header">
        <div>
          <h2>Application tracker</h2>
          <p>
            Monitor saved jobs, applications, interviews, follow-ups, and
            outcomes.
          </p>
        </div>
      </div>

      <div className="tracker-stats-grid">
        <div className="tracker-stat">
          <strong>{analytics.total_saved || 0}</strong>
          <span>Total saved</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.total_applied || 0}</strong>
          <span>Applied</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.interviews_scheduled || 0}</strong>
          <span>Interviews</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.offers_received || 0}</strong>
          <span>Offers</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.rejected_count || 0}</strong>
          <span>Rejected</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.pending_followups || 0}</strong>
          <span>Follow-ups</span>
        </div>
        <div className="tracker-stat">
          <strong>{analytics.application_conversion_rate || 0}%</strong>
          <span>Conversion</span>
        </div>
      </div>

      <div className="tracker-controls">
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          {STATUSES.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="updated_at">Updated date</option>
          <option value="applied_date">Applied date</option>
          <option value="follow_up_date">Follow-up date</option>
          <option value="company">Company</option>
          <option value="role">Role</option>
          <option value="status">Status</option>
        </select>

        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      {loading && <p className="muted">Loading tracker...</p>}
      {error && <div className="error-box">{error}</div>}

      <div className="tracker-table-card">
        {!data.applications?.length ? (
          <div className="empty-state">
            <p>
              No applications tracked yet. Save jobs from the job search page.
            </p>
          </div>
        ) : (
          <div className="tracker-table-wrap">
            <table className="tracker-table">
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Applied</th>
                  <th>Follow-up</th>
                  <th>Resume</th>
                  <th>Notes</th>
                  <th>Job</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {data.applications.map((item) => (
                  <tr key={item.id}>
                    <td>{item.company}</td>
                    <td>{item.role}</td>
                    <td>
                      <select
                        value={item.status}
                        onChange={(e) =>
                          handleStatusChange(item.id, e.target.value)
                        }
                      >
                        {STATUSES.filter((s) => s !== "All").map((s) => (
                          <option key={s} value={s}>
                            {s}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>{item.applied_date || "-"}</td>
                    <td>{item.follow_up_date || "-"}</td>
                    <td>{item.resume_version || "-"}</td>
                    <td>{item.notes || "-"}</td>
                    <td>
                      <a href={item.job_url} target="_blank" rel="noreferrer">
                        Open
                      </a>
                    </td>
                    <td>
                      <button
                        className="danger-btn"
                        onClick={() => handleDelete(item.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export default TrackerDashboard;
