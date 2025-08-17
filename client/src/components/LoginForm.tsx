import axios from "axios";
import React, { useState } from "react";
import type { UserData } from "../types/Interface";

interface LoginFormProps {
  onSwitchToSignUp: () => void;
  onLogin: (userData: UserData) => void;
}

function LoginForm({ onSwitchToSignUp, onLogin }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    axios
      .post("http://localhost:8000/login", {
        email,
        password,
      })
      .then((response) => {
        const userData: UserData = response.data;
        console.log("Login successful", userData);
        onLogin(userData);
      })
      .catch((error) => {
        console.log("Login failed", error);
        const errorMessage = error.response?.data?.detail;
        alert(errorMessage);
      });
  };

  return (
    <div className="login-section">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">
          Sign In
        </button>
      </form>
      <div className="login-footer">
        <span>Don't have an account? </span>
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            onSwitchToSignUp();
          }}
        >
          Create Account
        </a>
      </div>
    </div>
  );
}

export default LoginForm;
