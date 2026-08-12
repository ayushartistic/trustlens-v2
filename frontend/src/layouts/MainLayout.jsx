import { NavLink, Outlet } from "react-router-dom";
import "./MainLayout.css";

function MainLayout() {
  const navigation = [
    {
      section: "Overview",
      items: [
        { label: "Dashboard", path: "/" },
      ],
    },
    {
      section: "Social Data",
      items: [
        { label: "Users", path: "/users" },
        { label: "Posts", path: "/posts" },
        { label: "Comments", path: "/comments" },
      ],
    },
    {
      section: "Security",
      items: [
        { label: "Accounts", path: "/accounts" },
        { label: "Detections", path: "/detections" },
      ],
    },
    {
      section: "Simulation",
      items: [
        { label: "Attack Console", path: "/attacks" },
      ],
    },
  ];

  return (
    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-mark">T</div>

          <div>
            <div className="brand-name">TrustLens</div>
            <div className="brand-subtitle">
              Security Intelligence
            </div>
          </div>
        </div>

        <nav className="navigation">

          {navigation.map((group) => (
            <div className="nav-group" key={group.section}>

              <div className="nav-section-title">
                {group.section}
              </div>

              {group.items.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === "/"}
                  className={({ isActive }) =>
                    `nav-item ${isActive ? "active" : ""}`
                  }
                >
                  {item.label}
                </NavLink>
              ))}

            </div>
          ))}

        </nav>

        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot"></span>
            System Online
          </div>

          <div className="version">
            TrustLens v1.0
          </div>
        </div>

      </aside>

      <main className="main-content">

        <header className="topbar">

          <div>
            <div className="topbar-title">
              TrustLens
            </div>

            <div className="topbar-subtitle">
              Social Media Authenticity & Security Analysis
            </div>
          </div>

          <div className="backend-status">
            <span className="status-dot"></span>
            Backend Connected
          </div>

        </header>

        <section className="page-content">
          <Outlet />
        </section>

      </main>

    </div>
  );
}

export default MainLayout;