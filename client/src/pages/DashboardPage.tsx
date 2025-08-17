import type { UserData } from "../types/Interface";

interface DashboardPageProps {
  user: UserData | null;
  onLogout: () => void;
}

function DashboardPage({ user, onLogout }: DashboardPageProps) {
  return (
    <div>
      <h1>{user?.email}</h1>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default DashboardPage;
