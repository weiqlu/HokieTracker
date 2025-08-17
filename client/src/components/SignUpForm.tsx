import React, { useState } from "react";
import axios from "axios";

interface SignUpFormProps {
  onSwitchToLogin: () => void;
}

function SignUpForm({ onSwitchToLogin }: SignUpFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    axios
      .post("http://localhost:8000/signup", {
        email,
        password,
      })
      .then((response) => {
        // success message
        alert(response.data.message);

        // clear the form if signup is successful
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        onSwitchToLogin();
      })
      .catch((error) => {
        console.log("Signup failed", error);
        const errorMessage = error.response?.data?.detail;
        alert(errorMessage);
      });
    // need to add cases for existing emails, etc.
  };

  return (
    <div className="login-section">
      <h2>Create Account</h2>
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
        <div className="form-group">
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">
          Create Account
        </button>
      </form>
      <div className="login-footer">
        <span>Already have an account? </span>
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            onSwitchToLogin();
          }}
        >
          Sign In
        </a>
      </div>
    </div>
  );
}

export default SignUpForm;
