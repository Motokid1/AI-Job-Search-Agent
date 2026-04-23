import JobCard from "./JobCard";

function JobList({ jobs }) {
  return (
    <section className="jobs-panel">
      <div className="jobs-header">
        <h2>Matching Jobs</h2>
        <p>{jobs.length} result(s)</p>
      </div>

      {jobs.length === 0 ? (
        <div className="empty-state">
          <p>No jobs found for the current search.</p>
        </div>
      ) : (
        <div className="jobs-list">
          {jobs.map((job, index) => (
            <JobCard key={`${job.source_url}-${index}`} job={job} />
          ))}
        </div>
      )}
    </section>
  );
}

export default JobList;
