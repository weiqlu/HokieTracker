import { useState } from "react";
import LoginPage from "./pages/LoginPage";
import DashBoardPage from "./pages/DashboardPage";
import type { UserData } from "./types/Interface";

function App() {
  const [isLoggedIn, setisLoggedIn] = useState(false);
  const [user, setUser] = useState<UserData | null>(null);

  const handleLogin = (userData: UserData) => {
    setUser(userData);
    setisLoggedIn(true);
  };

  const handleLogout = () => {
    setUser(null);
    setisLoggedIn(false);
  };

  return (
    <div className="App">
      {isLoggedIn ? (
        <DashBoardPage user={user} onLogout={handleLogout} />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
