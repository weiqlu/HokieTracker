import { useState, useEffect } from "react";
import LoginPage from "./pages/LoginPage";
import DashBoardPage from "./pages/DashboardPage";
import { Routes, Route, Navigate } from "react-router";
import type { UserData } from "./types/Interface";

function App() {
  const [user, setUser] = useState<UserData | null>(null);

  // persist user so refresh doesn't kill the session
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData: UserData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <div className="App">
      <Routes>
        <Route
          path="/"
          element={
            !user ? (
              <LoginPage onLogin={handleLogin} />
            ) : (
              <Navigate to="/dashboard" />
            )
          }
        />
        <Route
          path="/dashboard"
          element={
            user ? (
              <DashBoardPage user={user} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
      </Routes>
    </div>
  );
}

export default App;
