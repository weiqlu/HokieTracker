import type { UserData } from "../types/Interface";
import "../styles/DashboardPage.css";

interface DashboardPageProps {
  user: UserData | null;
  onLogout: () => void;
}

function DashboardPage({ user, onLogout }: DashboardPageProps) {
  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1 className="dashboard-title">HokieTracker</h1>
        <button className="logout-button" onClick={onLogout}>
          Logout
        </button>
      </div>
      <div className="dashboard-content">
        <h2>Welcome, {user?.email}</h2>
        {/* Add your main dashboard content here */}
      </div>
    </div>
  );
}

export default DashboardPage;
