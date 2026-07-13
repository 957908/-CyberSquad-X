import { useState } from "react";
import { API_BASE_URL } from "../services/api";

function Login() {
  const [mode, setMode] = useState("login"); // "login" | "register" | "forgot"
  
  // Login States
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Register States
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [orgName, setOrgName] = useState("");
  const [mobileNumber, setMobileNumber] = useState("");
  const [regUsername, setRegUsername] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regSuccess, setRegSuccess] = useState("");

  // Recovery States
  const [recoverUsername, setRecoverUsername] = useState("");
  const [recoveryMethod, setRecoveryMethod] = useState("mobile"); // "mobile" | "email"
  const [otpCode, setOtpCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [recoveryStep, setRecoveryStep] = useState(1); // 1 | 2
  const [otpMockBackdoor, setOtpMockBackdoor] = useState("");

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
        setError(data.message || "Invalid username or password.");
      }
    } catch (err) {
      setError("Unable to connect to the security API.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!firstName || !lastName || !orgName || !mobileNumber || !regUsername || !regPassword) {
      setError("Please fill in all fields.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          work_organization: orgName,
          mobile_number: mobileNumber,
          username: regUsername,
          password: regPassword
        })
      });
      const data = await response.json();
      if (data.success) {
        setRegSuccess("Registration successful! Redirecting...");
        setFirstName("");
        setLastName("");
        setOrgName("");
        setMobileNumber("");
        setRegUsername("");
        setRegPassword("");
        setTimeout(() => {
          setMode("login");
          setRegSuccess("");
        }, 1500);
      } else {
        setError(data.message || "Registration failed.");
      }
    } catch (err) {
      setError("Unable to connect to the security API.");
    } finally {
      setLoading(false);
    }
  };

  const handleRecoveryRequest = async (e) => {
    e.preventDefault();
    if (!recoverUsername) {
      setError("Please enter your username.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/forgot-password/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: recoverUsername,
          method: recoveryMethod
        })
      });
      const data = await response.json();
      if (data.success) {
        setRecoveryStep(2);
        setOtpMockBackdoor(data.otp_mock || "");
        setError("");
      } else {
        setError(data.message || "Failed to send OTP.");
      }
    } catch (err) {
      setError("Unable to connect to the security API.");
    } finally {
      setLoading(false);
    }
  };

  const handleRecoveryVerify = async (e) => {
    e.preventDefault();
    if (!otpCode || !newPassword) {
      setError("Please enter the OTP and a new password.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/forgot-password/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: recoverUsername,
          otp: otpCode,
          new_password: newPassword
        })
      });
      const data = await response.json();
      if (data.success) {
        setRegSuccess("Password reset successfully! Redirecting...");
        setRecoverUsername("");
        setOtpCode("");
        setNewPassword("");
        setRecoveryStep(1);
        setOtpMockBackdoor("");
        setTimeout(() => {
          setMode("login");
          setRegSuccess("");
        }, 1500);
      } else {
        setError(data.message || "OTP verification failed.");
      }
    } catch (err) {
      setError("Unable to connect to the security API.");
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
        background: "var(--bg-darker)",
        fontFamily: "'Outfit', 'Inter', sans-serif",
        color: "var(--text-main)",
        padding: "20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "460px",
          background: "var(--bg-panel)",
          backdropFilter: "blur(12px)",
          border: "1px solid var(--border-color)",
          borderRadius: "16px",
          padding: "35px",
          boxShadow: "0 0 30px var(--shadow-color)",
          textAlign: "center",
        }}
      >
        <div style={{ marginBottom: "25px" }}>
          <div
            style={{
              display: "inline-flex",
              justifyContent: "center",
              alignItems: "center",
              width: "60px",
              height: "60px",
              background: "rgba(6, 182, 212, 0.1)",
              border: "1px solid var(--border-color)",
              borderRadius: "50%",
              marginBottom: "15px",
              fontSize: "28px",
              color: "var(--accent-cyan)",
            }}
          >
            🛡️
          </div>
          <h1
            style={{
              fontSize: "26px",
              fontWeight: "700",
              margin: "0 0 5px 0",
              color: "var(--text-white)",
            }}
          >
            CyberSquad X
          </h1>
          <p style={{ fontSize: "14px", color: "var(--text-gray)", margin: 0 }}>
            {mode === "login" && "Secure Operations Portal"}
            {mode === "register" && "Create Security Operator Account"}
            {mode === "forgot" && "Reset Credentials Gateway"}
          </p>
        </div>

        {error && (
          <div
            style={{
              background: "rgba(239, 68, 68, 0.1)",
              border: "1px solid rgba(239, 68, 68, 0.3)",
              color: "#f87171",
              padding: "12px",
              borderRadius: "8px",
              fontSize: "14px",
              marginBottom: "20px",
              textAlign: "left",
            }}
          >
            ⚠️ {error}
          </div>
        )}

        {regSuccess && (
          <div
            style={{
              background: "rgba(34, 197, 94, 0.1)",
              border: "1px solid rgba(34, 197, 94, 0.3)",
              color: "#4ade80",
              padding: "12px",
              borderRadius: "8px",
              fontSize: "14px",
              marginBottom: "20px",
              textAlign: "left",
            }}
          >
            ✅ {regSuccess}
          </div>
        )}

        {/* LOGIN MODE */}
        {mode === "login" && (
          <form onSubmit={login} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "13px", color: "var(--text-gray)", fontWeight: "500" }}>Username / Email</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                style={{ marginTop: "6px", width: "100%", maxWidth: "none" }}
              />
            </div>

            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "13px", color: "var(--text-gray)", fontWeight: "500" }}>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{ marginTop: "6px", width: "100%", maxWidth: "none" }}
              />
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", fontSize: "13px" }}>
              <span
                onClick={() => { setMode("forgot"); setError(""); }}
                style={{ color: "var(--accent-cyan)", cursor: "pointer", fontWeight: "600" }}
              >
                Forgot Password?
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                padding: "13px",
                background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                border: "none",
                borderRadius: "8px",
                color: "white",
                fontWeight: "700",
                fontSize: "15px",
                cursor: "pointer",
                boxShadow: "0 4px 12px rgba(6, 182, 212, 0.25)",
              }}
            >
              {loading ? "Authenticating..." : "Establish Secure Session"}
            </button>

            <div style={{ fontSize: "14px", marginTop: "10px", color: "var(--text-gray)" }}>
              New user?{" "}
              <span
                onClick={() => { setMode("register"); setError(""); }}
                style={{ color: "var(--accent-cyan)", cursor: "pointer", fontWeight: "600" }}
              >
                Register here
              </span>
            </div>
          </form>
        )}

        {/* REGISTER MODE */}
        {mode === "register" && (
          <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
              <div style={{ textAlign: "left" }}>
                <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>First Name</label>
                <input
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="John"
                  style={{ marginTop: "4px", width: "100%" }}
                />
              </div>
              <div style={{ textAlign: "left" }}>
                <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>Last Name</label>
                <input
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Doe"
                  style={{ marginTop: "4px", width: "100%" }}
                />
              </div>
            </div>

            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>Work Organization</label>
              <input
                type="text"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                placeholder="Defense Systems / Cyber Inc."
                style={{ marginTop: "4px", width: "100%" }}
              />
            </div>

            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>Mobile Number</label>
              <input
                type="tel"
                value={mobileNumber}
                onChange={(e) => setMobileNumber(e.target.value)}
                placeholder="+1234567890"
                style={{ marginTop: "4px", width: "100%" }}
              />
            </div>

            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>Username (Email / ID)</label>
              <input
                type="text"
                value={regUsername}
                onChange={(e) => setRegUsername(e.target.value)}
                placeholder="johndoe@cybersquad.com"
                style={{ marginTop: "4px", width: "100%" }}
              />
            </div>

            <div style={{ textAlign: "left" }}>
              <label style={{ fontSize: "12px", color: "var(--text-gray)" }}>Access Password</label>
              <input
                type="password"
                value={regPassword}
                onChange={(e) => setRegPassword(e.target.value)}
                placeholder="••••••••"
                style={{ marginTop: "4px", width: "100%" }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                padding: "13px",
                background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                border: "none",
                borderRadius: "8px",
                color: "white",
                fontWeight: "700",
                fontSize: "15px",
                cursor: "pointer",
                boxShadow: "0 4px 12px rgba(6, 182, 212, 0.25)",
                marginTop: "5px"
              }}
            >
              {loading ? "Creating..." : "Submit Registration"}
            </button>

            <div style={{ fontSize: "14px", marginTop: "5px", color: "var(--text-gray)" }}>
              Already registered?{" "}
              <span
                onClick={() => { setMode("login"); setError(""); }}
                style={{ color: "var(--accent-cyan)", cursor: "pointer", fontWeight: "600" }}
              >
                Log in here
              </span>
            </div>
          </form>
        )}

        {/* FORGOT PASSWORD MODE */}
        {mode === "forgot" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
            {recoveryStep === 1 ? (
              <form onSubmit={handleRecoveryRequest} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ textAlign: "left" }}>
                  <label style={{ fontSize: "13px", color: "var(--text-gray)" }}>Operator Username (Email)</label>
                  <input
                    type="text"
                    value={recoverUsername}
                    onChange={(e) => setRecoverUsername(e.target.value)}
                    placeholder="email@domain.com"
                    style={{ marginTop: "6px", width: "100%" }}
                  />
                </div>

                <div style={{ textAlign: "left" }}>
                  <label style={{ fontSize: "13px", color: "var(--text-gray)" }}>Choose OTP Delivery Channel</label>
                  <div style={{ display: "flex", gap: "10px", marginTop: "8px" }}>
                    <button
                      type="button"
                      onClick={() => setRecoveryMethod("mobile")}
                      style={{
                        flex: 1,
                        padding: "10px",
                        background: recoveryMethod === "mobile" ? "rgba(6, 182, 212, 0.15)" : "transparent",
                        border: recoveryMethod === "mobile" ? "1px solid #06b6d4" : "1px solid var(--border-color)",
                        borderRadius: "8px",
                        color: "white",
                        cursor: "pointer",
                        fontWeight: "600",
                        fontSize: "13px"
                      }}
                    >
                      📱 Mobile Number OTP
                    </button>
                    <button
                      type="button"
                      onClick={() => setRecoveryMethod("email")}
                      style={{
                        flex: 1,
                        padding: "10px",
                        background: recoveryMethod === "email" ? "rgba(6, 182, 212, 0.15)" : "transparent",
                        border: recoveryMethod === "email" ? "1px solid #06b6d4" : "1px solid var(--border-color)",
                        borderRadius: "8px",
                        color: "white",
                        cursor: "pointer",
                        fontWeight: "600",
                        fontSize: "13px"
                      }}
                    >
                      ✉️ Email Address OTP
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  style={{
                    width: "100%",
                    padding: "13px",
                    background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                    border: "none",
                    borderRadius: "8px",
                    color: "white",
                    fontWeight: "700",
                    fontSize: "15px",
                    cursor: "pointer",
                    boxShadow: "0 4px 12px rgba(6, 182, 212, 0.25)",
                  }}
                >
                  {loading ? "Sending..." : "Request Verification Code"}
                </button>
              </form>
            ) : (
              <form onSubmit={handleRecoveryVerify} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ background: "rgba(6, 182, 212, 0.05)", border: "1px solid var(--border-color)", padding: "12px", borderRadius: "8px", textAlign: "left" }}>
                  <p style={{ margin: 0, fontSize: "13px", color: "var(--text-main)" }}>
                    An OTP Code has been dispatched via <strong>{recoveryMethod}</strong>.
                  </p>
                  {otpMockBackdoor && (
                    <p style={{ margin: "5px 0 0", fontSize: "12px", color: "var(--accent-cyan)" }}>
                      🔑 Test OTP Gateway: <strong>{otpMockBackdoor}</strong> (logged on server console)
                    </p>
                  )}
                </div>

                <div style={{ textAlign: "left" }}>
                  <label style={{ fontSize: "13px", color: "var(--text-gray)" }}>6-Digit OTP Code</label>
                  <input
                    type="text"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value)}
                    placeholder="123456"
                    style={{ marginTop: "6px", width: "100%", letterSpacing: "4px", textAlign: "center", fontSize: "16px", fontWeight: "700" }}
                  />
                </div>

                <div style={{ textAlign: "left" }}>
                  <label style={{ fontSize: "13px", color: "var(--text-gray)" }}>Set New Secure Password</label>
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="••••••••"
                    style={{ marginTop: "6px", width: "100%" }}
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  style={{
                    width: "100%",
                    padding: "13px",
                    background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                    border: "none",
                    borderRadius: "8px",
                    color: "white",
                    fontWeight: "700",
                    fontSize: "15px",
                    cursor: "pointer",
                    boxShadow: "0 4px 12px rgba(6, 182, 212, 0.25)",
                  }}
                >
                  {loading ? "Updating..." : "Verify & Reset Password"}
                </button>
              </form>
            )}

            <div style={{ fontSize: "14px", marginTop: "5px", color: "var(--text-gray)" }}>
              Back to{" "}
              <span
                onClick={() => { setMode("login"); setError(""); setRecoveryStep(1); }}
                style={{ color: "var(--accent-cyan)", cursor: "pointer", fontWeight: "600" }}
              >
                Log In
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Login;