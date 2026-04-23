import FitScoreCard from "./FitScoreCard";
import GapReport from "./GapReport";
import ResumeSuggestions from "./ResumeSuggestions";
import CareerSuggestions from "./CareerSuggestions";
import LearningResources from "./LearningResources";

function AnalysisDashboard({ data }) {
  return (
    <div className="analysis-dashboard">
      <div className="analysis-overview-card">
        <h2>Resume Analysis Overview</h2>
        <p>
          <strong>Target Role:</strong> {data.target_role}
        </p>
        <p>
          <strong>Package:</strong>{" "}
          {data.package_min_lpa || data.package_max_lpa
            ? `${data.package_min_lpa || "-"} - ${data.package_max_lpa || "-"} LPA`
            : "Not specified"}
        </p>
        <p>
          <strong>Location:</strong> {data.location || "Not specified"}
        </p>
        <p>
          <strong>Companies:</strong>{" "}
          {data.companies?.length ? data.companies.join(", ") : "Not specified"}
        </p>
        <p>
          <strong>Target Domain:</strong>{" "}
          {data.target_domain || "Not specified"}
        </p>
        <p className="analysis-final-recommendation">
          {data.final_recommendation}
        </p>
      </div>

      <FitScoreCard fit={data.fit_analysis} />
      <GapReport gap={data.gap_report} />
      <ResumeSuggestions data={data.resume_modifications} />
      <CareerSuggestions data={data.career_growth_suggestions} />
      <LearningResources resources={data.learning_resources || []} />
    </div>
  );
}

export default AnalysisDashboard;
