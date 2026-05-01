import JobCard from "./JobCard";

function JobList({ jobs, onAnalyzeJob }) {
  return (
    <section className="jobs-panel">
      <div className="jobs-header">
        <div>
          <h2>Recommended roles</h2>
          <p>{jobs.length} role(s) found based on your profile</p>
        </div>
      </div>

      {jobs.length === 0 ? (
        <div className="empty-state">
          <p>
            No jobs found. Try adding more skills, a broader location, or a
            different role title.
          </p>
        </div>
      ) : (
        <div className="jobs-list">
          {jobs.map((job, index) => (
            <JobCard
              key={`${job.source_url}-${index}`}
              job={job}
              onAnalyzeJob={onAnalyzeJob}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default JobList;
