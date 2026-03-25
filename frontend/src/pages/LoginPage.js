import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const endpoint = isRegistering ? "/api/auth/register" : "/api/auth/login";

    try {
      const res = await api.post(endpoint, { username, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/students");
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map((e) => e.msg).join(", "));
      } else {
        setError(detail || "Authentication failed");
      }
    }
  };

  return (
    <div className="card" style={{ maxWidth: 420, margin: "4rem auto" }}>
      <h2>{isRegistering ? "Register" : "Login"}</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className="btn" type="submit">
          {isRegistering ? "Register" : "Login"}
        </button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        {isRegistering ? "Already have an account?" : "No account?"}{" "}
        <button
          style={{ background: "none", border: "none", color: "#1a73e8", cursor: "pointer" }}
          onClick={() => setIsRegistering(!isRegistering)}
        >
          {isRegistering ? "Login" : "Register"}
        </button>
      </p>
    </div>
  );
}
