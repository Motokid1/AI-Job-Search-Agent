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
    setSelectedJob(job);
    setJobMatchOpen(true);
  };

  const handleCloseJobMatch = () => {
    setSelectedJob(null);
    setJobMatchOpen(false);
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
                  requirements, and evaluate your resume against specific job
                  descriptions before applying.
                </p>
              </div>
              <div className="hero-metrics">
                <div>
                  <strong>6</strong>
                  <span>Curated results</span>
                </div>
                <div>
                  <strong>AI</strong>
                  <span>Resume matching</span>
                </div>
                <div>
                  <strong>JD</strong>
                  <span>Specific scoring</span>
                </div>
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
                    className={jobInputMode === "resume" ? "active" : ""}
                    onClick={() => setJobInputMode("resume")}
                  >
                    Resume
                  </button>
                  <button
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
                <JobList jobs={jobs} onAnalyzeJob={handleOpenJobMatch} />
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
      </main>

      {jobMatchOpen && selectedJob && (
        <JobMatchModal job={selectedJob} onClose={handleCloseJobMatch} />
      )}
    </div>
  );
}

export default App;
