function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs">
      <button
        className={activeTab === "resume" ? "tab active" : "tab"}
        onClick={() => setActiveTab("resume")}
      >
        Resume Upload
      </button>
      <button
        className={activeTab === "manual" ? "tab active" : "tab"}
        onClick={() => setActiveTab("manual")}
      >
        Manual Input
      </button>
    </div>
  );
}

export default Tabs;
