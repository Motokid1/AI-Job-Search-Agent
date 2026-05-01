function Header({ activePage, setActivePage }) {
  return (
    <header className="topbar">
      <div className="topbar-inner container">
        <div className="brand-block">
          <div className="brand-logo">JA</div>
          <div>
            <h2 className="brand-title">JobAlign AI</h2>
            <p className="brand-subtitle">
              AI job discovery and resume intelligence
            </p>
          </div>
        </div>

        <nav className="top-nav">
          <button
            className={activePage === "jobs" ? "nav-link active" : "nav-link"}
            onClick={() => setActivePage("jobs")}
          >
            Job Search
          </button>
          <button
            className={
              activePage === "analysis" ? "nav-link active" : "nav-link"
            }
            onClick={() => setActivePage("analysis")}
          >
            Resume Analysis
          </button>
        </nav>
      </div>
    </header>
  );
}

export default Header;
