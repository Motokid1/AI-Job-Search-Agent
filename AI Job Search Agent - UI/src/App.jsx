import { useState } from "react";
import Header from "./components/Header";
import ResumeUploadForm from "./components/ResumeUploadForm";
import ManualSearchForm from "./components/ManualSearchForm";
import JobList from "./components/JobList";
import ProfileSummary from "./components/ProfileSummary";
import LoadingSpinner from "./components/LoadingSpinner";
import ErrorMessage from "./components/ErrorMessage";

import AnalysisForm from "./components/analysis/AnalysisForm";
import AnalysisDashboard from "./components/analysis/AnalysisDashboard";

import JobMatchModal from "./components/match/JobMatchModal";
import AutoApplyModal from "./components/apply/AutoApplyModal";

import TrackerDashboard from "./components/tracker/TrackerDashboard";
import SaveToTrackerModal from "./components/tracker/SaveToTrackerModal";

function App() {
  const [activePage, setActivePage] = useState("jobs");
  const [jobInputMode, setJobInputMode] = useState("resume");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [jobs, setJobs] = useState([]);
  const [profile, setProfile] = useState(null);
  const [totalFound, setTotalFound] = useState(0);

  const [analysisData, setAnalysisData] = useState(null);

  const [selectedJob, setSelectedJob] = useState(null);
  const [jobMatchOpen, setJobMatchOpen] = useState(false);

  const [applyJob, setApplyJob] = useState(null);
  const [applyOpen, setApplyOpen] = useState(false);

  const [trackerJob, setTrackerJob] = useState(null);
  const [trackerOpen, setTrackerOpen] = useState(false);

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
    setLoading(false);
    setAnalysisData(data);
  };

  const handleAnalysisError = (message) => {
    setLoading(false);
    setAnalysisData(null);
    setError(message || "Analysis failed.");
  };

  const handleOpenJobMatch = (job) => {
    console.log("Opening job match modal:", job);
    setSelectedJob(job);
    setJobMatchOpen(true);
  };

  const handleCloseJobMatch = () => {
    setSelectedJob(null);
    setJobMatchOpen(false);
  };

  const handleOpenApplyAssistant = (job) => {
    console.log("Opening apply assistant:", job);
    setApplyJob(job);
    setApplyOpen(true);
  };

  const handleCloseApplyAssistant = () => {
    setApplyJob(null);
    setApplyOpen(false);
  };

  const handleOpenTracker = (job) => {
    console.log("Opening tracker modal:", job);
    setTrackerJob(job);
    setTrackerOpen(true);
  };

  const handleCloseTracker = () => {
    setTrackerJob(null);
    setTrackerOpen(false);
  };

  return (
    <div className="app-shell">
      <Header activePage={activePage} setActivePage={setActivePage} />

      <main className="container">
        {activePage === "jobs" && (
          <>
            <section className="hero-card product-hero">
              <div>
                <span className="eyebrow">AI-powered career discovery</span>
                <h1>Find better-fit jobs with intelligent resume matching.</h1>
                <p>
                  Search relevant roles, compare your profile with job
                  requirements, prepare application material, and track every
                  job application.
                </p>
              </div>
            </section>

            <section className="panel">
              <div className="section-header">
                <div>
                  <h2>Search jobs</h2>
                  <p>Use your resume or enter your profile details manually.</p>
                </div>

                <div className="segmented-control">
                  <button
                    type="button"
                    className={jobInputMode === "resume" ? "active" : ""}
                    onClick={() => setJobInputMode("resume")}
                  >
                    Resume
                  </button>

                  <button
                    type="button"
                    className={jobInputMode === "manual" ? "active" : ""}
                    onClick={() => setJobInputMode("manual")}
                  >
                    Manual
                  </button>
                </div>
              </div>

              {jobInputMode === "resume" ? (
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

            {loading && <LoadingSpinner text="Finding relevant jobs..." />}
            {error && <ErrorMessage message={error} />}

            {!loading && (profile || jobs.length > 0) && (
              <section className="results-grid">
                {profile && (
                  <ProfileSummary profile={profile} totalFound={totalFound} />
                )}

                <JobList
                  jobs={jobs}
                  onAnalyzeJob={handleOpenJobMatch}
                  onPrepareApply={handleOpenApplyAssistant}
                  onSaveToTracker={handleOpenTracker}
                />
              </section>
            )}
          </>
        )}

        {activePage === "analysis" && (
          <>
            <section className="hero-card product-hero">
              <div>
                <span className="eyebrow">Resume intelligence</span>
                <h1>
                  Understand how ready your resume is for your target role.
                </h1>
                <p>
                  Analyze role readiness, skill gaps, ATS alignment, resume
                  improvements, and learning resources based on your career
                  goal.
                </p>
              </div>
            </section>

            <section className="panel">
              <div className="section-header">
                <div>
                  <h2>Analyze resume</h2>
                  <p>Upload your resume and define your target role.</p>
                </div>
              </div>

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

        {activePage === "tracker" && (
          <>
            <section className="hero-card product-hero">
              <div>
                <span className="eyebrow">Application management</span>
                <h1>Track every job application in one place.</h1>
                <p>
                  Monitor saved jobs, applications, interviews, follow-ups,
                  offers, and outcomes with a simple job search pipeline.
                </p>
              </div>
            </section>

            <TrackerDashboard />
          </>
        )}
      </main>

      {jobMatchOpen && selectedJob && (
        <JobMatchModal job={selectedJob} onClose={handleCloseJobMatch} />
      )}

      {applyOpen && applyJob && (
        <AutoApplyModal job={applyJob} onClose={handleCloseApplyAssistant} />
      )}

      {trackerOpen && trackerJob && (
        <SaveToTrackerModal job={trackerJob} onClose={handleCloseTracker} />
      )}
    </div>
  );
}

export default App;
