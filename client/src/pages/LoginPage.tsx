import { useState } from "react";
import LoginForm from "../components/LoginForm";
import SignUpForm from "../components/SignUpForm";
import "../styles/LoginPage.css";

interface LoginPageProps {
  onLogin: (userData: any) => void;
}

function LoginPage({ onLogin }: LoginPageProps) {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className="login-overlay">
      <div className="login-modal">
        {/* app introduction */}
        <div className="app-info">
          <h1 className="app-title">HOKIETRACKER</h1>
          <p>
            Get notified the moment seats open in your Virginia Tech courses.
            Stop refreshing the timetable - we'll watch it for you
          </p>
          <p className="timetable-reference">
            Refer to the{" "}
            <a
              href="https://selfservice.banner.vt.edu/ssb/HZSKVTSC.P_DispRequest"
              target="_blank"
              rel="noopener noreferrer"
              className="timetable-link"
            >
              Timetable of Classes
            </a>{" "}
            for official course listings
          </p>
          <div className="features">
            <div className="feature">
              <span className="feature-icon">📋</span>
              <span>Course Tracking</span>
            </div>
            <div className="feature">
              <span className="feature-icon">🔔</span>
              <span>Instant Notifications</span>
            </div>
            <div className="feature">
              <span className="feature-icon">⚡</span>
              <span>Real-time Updates</span>
            </div>
          </div>
        </div>

        {/* login/signup form  */}
        {isSignUp ? (
          <SignUpForm onSwitchToLogin={() => setIsSignUp(false)} />
        ) : (
          <LoginForm
            onSwitchToSignUp={() => setIsSignUp(true)}
            onLogin={onLogin}
          />
        )}
      </div>
    </div>
  );
}

export default LoginPage;
