import { useState } from "react";
import { API_BASE_URL } from "../services/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("Please fill in all fields.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("role", data.role); // Save user role for route guards
        window.location = "/";
      } else {
        setError("Invalid username or password.");
      }
    } catch (err) {
      setError("Unable to connect to the security API.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "radial-gradient(circle at center, #111827 0%, #030712 100%)",
        fontFamily: "'Outfit', 'Inter', sans-serif",
        color: "#f3f4f6",
        padding: "20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "420px",
          background: "rgba(17, 24, 39, 0.7)",
          backdropFilter: "blur(12px)",
          border: "1px solid rgba(6, 182, 212, 0.2)",
          borderRadius: "16px",
          padding: "40px",
          boxShadow: "0 0 30px rgba(6, 182, 212, 0.15), 0 10px 15px -3px rgba(0, 0, 0, 0.5)",
          textAlign: "center",
        }}
      >
        <div style={{ marginBottom: "30px" }}>
          <div
            style={{
              display: "inline-flex",
              justifyContent: "center",
              alignItems: "center",
              width: "64px",
              height: "64px",
              background: "rgba(6, 182, 212, 0.1)",
              border: "1px solid rgba(6, 182, 212, 0.4)",
              borderRadius: "50%",
              marginBottom: "15px",
              fontSize: "32px",
              color: "#06b6d4",
              boxShadow: "0 0 15px rgba(6, 182, 212, 0.3)",
            }}
          >
            🛡️
          </div>
          <h1
            style={{
              fontSize: "28px",
              fontWeight: "700",
              margin: "0 0 5px 0",
              background: "linear-gradient(135deg, #ffffff 0%, #a5f3fc 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              letterSpacing: "1px",
            }}
          >
            CYBER SQUAD X
          </h1>
          <p style={{ fontSize: "14px", color: "#9ca3af", margin: 0 }}>
            AI-Powered Security Operations Platform
          </p>
        </div>

        <form onSubmit={login}>
          {error && (
            <div
              style={{
                background: "rgba(239, 68, 68, 0.1)",
                border: "1px solid rgba(239, 68, 68, 0.3)",
                color: "#f87171",
                padding: "10px 12px",
                borderRadius: "8px",
                fontSize: "14px",
                marginBottom: "20px",
                textAlign: "left",
              }}
            >
              ⚠️ {error}
            </div>
          )}

          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                fontSize: "12px",
                fontWeight: "600",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: "#9ca3af",
                marginBottom: "8px",
              }}
            >
              Username / Identity
            </label>
            <input
              type="text"
              value={username}
              placeholder="Enter your security identity"
              onChange={(e) => setUsername(e.target.value)}
              style={{
                width: "100%",
                padding: "12px 16px",
                borderRadius: "8px",
                border: "1px solid #374151",
                background: "#1f2937",
                color: "white",
                fontSize: "15px",
                boxSizing: "border-box",
                transition: "all 0.2s ease",
                outline: "none",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#06b6d4")}
              onBlur={(e) => (e.target.style.borderColor = "#374151")}
            />
          </div>

          <div style={{ marginBottom: "30px", textAlign: "left" }}>
            <label
              style={{
                display: "block",
                fontSize: "12px",
                fontWeight: "600",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: "#9ca3af",
                marginBottom: "8px",
              }}
            >
              Access Cryptokey (Password)
            </label>
            <input
              type="password"
              value={password}
              placeholder="••••••••"
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "12px 16px",
                borderRadius: "8px",
                border: "1px solid #374151",
                background: "#1f2937",
                color: "white",
                fontSize: "15px",
                boxSizing: "border-box",
                transition: "all 0.2s ease",
                outline: "none",
              }}
              onFocus={(e) => (e.target.style.borderColor = "#06b6d4")}
              onBlur={(e) => (e.target.style.borderColor = "#374151")}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
              border: "none",
              borderRadius: "8px",
              color: "white",
              fontSize: "16px",
              fontWeight: "700",
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(6, 182, 212, 0.3)",
              transition: "all 0.2s ease",
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Authenticating..." : "Establish Secure Session"}
          </button>
        </form>

        <div style={{ marginTop: "25px", fontSize: "12px", color: "#6b7280" }}>
          This system is restricted to authorized personnel. Scan and assessment data is logged and encrypted.
        </div>
      </div>
    </div>
  );
}

export default Login;