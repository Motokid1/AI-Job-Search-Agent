import { useState } from "react";
import Header from "./components/Header";
import Tabs from "./components/Tabs";
import ResumeUploadForm from "./components/ResumeUploadForm";
import ManualSearchForm from "./components/ManualSearchForm";
import JobList from "./components/JobList";
import ProfileSummary from "./components/ProfileSummary";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorMessage from "./components/ErrorMessage";

import AnalysisForm from "./components/analysis/AnalysisForm";
import AnalysisDashboard from "./components/analysis/AnalysisDashboard";
import JobMatchModal from "./components/match/JobMatchModal";

function App() {
  const [mainTab, setMainTab] = useState("jobs");
  const [jobTab, setJobTab] = useState("resume");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [jobs, setJobs] = useState([]);
  const [profile, setProfile] = useState(null);
  const [totalFound, setTotalFound] = useState(0);

  const [analysisData, setAnalysisData] = useState(null);

  const [selectedJob, setSelectedJob] = useState(null);
  const [jobMatchOpen, setJobMatchOpen] = useState(false);

  const resetJobResults = () => {
    setJobs([]);
    setProfile(null);
    setTotalFound(0);
    setError("");
  };

  const resetAnalysisResults = () => {
    setAnalysisData(null);
    setError("");
  };

  const handleSearchStart = () => {
    setLoading(true);
    setError("");
  };

  const handleSearchSuccess = (data) => {
    console.log("JOB RESPONSE:", data);
    setLoading(false);
    setJobs(data.jobs || []);
    setProfile(data.profile || null);
    setTotalFound(data.total_found || 0);
  };

  const handleSearchError = (message) => {
    setLoading(false);
    setJobs([]);
    setProfile(null);
    setTotalFound(0);
    setError(message || "Something went wrong.");
  };

  const handleAnalysisStart = () => {
    setLoading(true);
    setError("");
  };

  const handleAnalysisSuccess = (data) => {
    console.log("ANALYSIS RESPONSE:", data);
    setLoading(false);
    setAnalysisData(data);
  };

  const handleAnalysisError = (message) => {
    setLoading(false);
    setAnalysisData(null);
    setError(message || "Analysis failed.");
  };

  const handleOpenJobMatch = (job) => {
    setSelectedJob(job);
    setJobMatchOpen(true);
  };

  const handleCloseJobMatch = () => {
    setSelectedJob(null);
    setJobMatchOpen(false);
  };

  return (
    <div className="app-shell">
      <Header />

      <main className="container">
        <section className="hero-card">
          <h1>AI Job Search Agent</h1>
          <p>
            Search jobs in Checkpoint - I, analyze resume fit in Checkpoint -
            II, and now match your resume against one exact job posting.
          </p>
        </section>

        <div className="main-tabs">
          <button
            className={mainTab === "jobs" ? "main-tab active" : "main-tab"}
            onClick={() => {
              setMainTab("jobs");
              setError("");
            }}
          >
            Checkpoint - I: Job Search
          </button>

          <button
            className={mainTab === "analysis" ? "main-tab active" : "main-tab"}
            onClick={() => {
              setMainTab("analysis");
              setError("");
            }}
          >
            Checkpoint - II: Resume Analysis
          </button>
        </div>

        {mainTab === "jobs" && (
          <>
            <Tabs activeTab={jobTab} setActiveTab={setJobTab} />

            <section className="panel">
              {jobTab === "resume" ? (
                <ResumeUploadForm
                  onSearchStart={handleSearchStart}
                  onSearchSuccess={handleSearchSuccess}
                  onSearchError={handleSearchError}
                  onReset={resetJobResults}
                />
              ) : (
                <ManualSearchForm
                  onSearchStart={handleSearchStart}
                  onSearchSuccess={handleSearchSuccess}
                  onSearchError={handleSearchError}
                  onReset={resetJobResults}
                />
              )}
            </section>

            {loading && (
              <LoadingSpinner text="Searching jobs and analyzing results..." />
            )}

            {error && <ErrorMessage message={error} />}

            {!loading && (profile || jobs.length > 0) && (
              <section className="results-grid">
                {profile && (
                  <ProfileSummary profile={profile} totalFound={totalFound} />
                )}

                <JobList jobs={jobs} onAnalyzeJob={handleOpenJobMatch} />
              </section>
            )}
          </>
        )}

        {mainTab === "analysis" && (
          <>
            <section className="panel">
              <AnalysisForm
                onAnalysisStart={handleAnalysisStart}
                onAnalysisSuccess={handleAnalysisSuccess}
                onAnalysisError={handleAnalysisError}
                onReset={resetAnalysisResults}
              />
            </section>

            {loading && <LoadingSpinner text="Analyzing resume..." />}

            {error && <ErrorMessage message={error} />}

            {!loading && analysisData && (
              <section className="analysis-section">
                <AnalysisDashboard data={analysisData} />
              </section>
            )}
          </>
        )}
      </main>

      {jobMatchOpen && selectedJob && (
        <JobMatchModal job={selectedJob} onClose={handleCloseJobMatch} />
      )}
    </div>
  );
}

export default App;
