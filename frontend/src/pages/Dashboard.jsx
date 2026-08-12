import { useEffect, useState } from "react";
import { getDashboardSummary } from "../api";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await getDashboardSummary();

        console.log("Dashboard data received:", data);

        setSummary(data);
      } catch (err) {
        console.error("Dashboard loading error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        Loading dashboard...
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-error">
        Failed to load dashboard: {error}
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="page-error">
        No dashboard data received.
      </div>
    );
  }

  const totalThreats =
    summary.comment_detections +
    summary.account_detections;

  return (
    <div className="dashboard-page">

      {/* PAGE HEADER */}
      <div className="page-header">
        <div>
          <h1>Security Dashboard</h1>

          <p>
            Overview of social-media activity, threats and
            detection results.
          </p>
        </div>
      </div>


      {/* STATISTICS */}
      <div className="stats-grid">

        {/* USERS */}
        <div className="stat-card">
          <div className="stat-label">
            Users
          </div>

          <div className="stat-value">
            {summary.users}
          </div>

          <div className="stat-description">
            Registered accounts
          </div>
        </div>


        {/* POSTS */}
        <div className="stat-card">
          <div className="stat-label">
            Posts
          </div>

          <div className="stat-value">
            {summary.posts}
          </div>

          <div className="stat-description">
            Social-media posts
          </div>
        </div>


        {/* COMMENTS */}
        <div className="stat-card">
          <div className="stat-label">
            Comments
          </div>

          <div className="stat-value">
            {summary.comments}
          </div>

          <div className="stat-description">
            User-generated comments
          </div>
        </div>


        {/* THREATS */}
        <div className="stat-card">
          <div className="stat-label">
            Threats
          </div>

          <div className="stat-value">
            {totalThreats}
          </div>

          <div className="stat-description">
            Detected security risks
          </div>
        </div>

      </div>


      {/* LOWER DASHBOARD */}
      <div className="dashboard-grid">

        {/* THREAT OVERVIEW */}
        <div className="dashboard-panel">

          <h2>
            Threat Overview
          </h2>

          <div className="threat-summary">

            <div className="threat-item">
              <span>
                Comment detections
              </span>

              <strong>
                {summary.comment_detections}
              </strong>
            </div>


            <div className="threat-item">
              <span>
                Account detections
              </span>

              <strong>
                {summary.account_detections}
              </strong>
            </div>


            <div className="threat-item">
              <span>
                Recorded attacks
              </span>

              <strong>
                {summary.attacks}
              </strong>
            </div>

          </div>

        </div>


        {/* RECENT ACTIVITY */}
        <div className="dashboard-panel">

          <h2>
            Recent Activity
          </h2>

          <div className="activity-summary">

            <div className="activity-item">
              <span>
                Attack events
              </span>

              <strong>
                {summary.attack_events}
              </strong>
            </div>


            <div className="activity-item">
              <span>
                Follow relationships
              </span>

              <strong>
                {summary.follows}
              </strong>
            </div>


            <div className="activity-item">
              <span>
                Social contexts
              </span>

              <strong>
                {summary.contexts}
              </strong>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;