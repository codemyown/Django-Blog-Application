import React, { useState } from "react";
import { loginUser } from "../api";

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    const result = await loginUser(username, password);

    if (result.access) {
      // Store tokens
      localStorage.setItem("access_token", result.access);
      localStorage.setItem("refresh_token", result.refresh);

      // Decode token to get expiry timestamp
      const decoded = JSON.parse(atob(result.access.split(".")[1]));
      localStorage.setItem("token_exp", decoded.exp); // UNIX timestamp in seconds

      setMessage("✅ Login successful!");
      if (onLogin) onLogin(); // 🔥 notify parent component (App)
    } else {
      setMessage(
        "❌ Login failed: " + (result.detail || "Invalid credentials")
      );
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Log In</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default LoginForm;
