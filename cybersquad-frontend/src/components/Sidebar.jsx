import { useState } from "react";

function Sidebar() {
  const [activeTab, setActiveTab] = useState("Dashboard");

  const menuItems = [
    { name: "Dashboard", icon: "📊" },
    { name: "History", icon: "📜" },
    { name: "Reports", icon: "📄" },
    { name: "CVE Center", icon: "🚨" },
    { name: "OWASP Top 10", icon: "🛡️" },
    { name: "Settings", icon: "⚙️" },
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    window.location = "/login";
  };

  return (
    <div
      style={{
        width: "250px",
        height: "100vh",
        background: "linear-gradient(180deg, #090d16 0%, #030712 100%)",
        color: "white",
        padding: "30px 20px",
        position: "fixed",
        left: 0,
        top: 0,
        borderRight: "1px solid rgba(6, 182, 212, 0.1)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        boxShadow: "4px 0 24px rgba(0, 0, 0, 0.4)",
        fontFamily: "'Outfit', sans-serif",
        zIndex: 100,
      }}
    >
      <div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            marginBottom: "35px",
            padding: "0 10px",
          }}
        >
          <span style={{ fontSize: "24px" }}>🛡️</span>
          <h2
            style={{
              fontSize: "20px",
              fontWeight: "800",
              background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              letterSpacing: "0.5px",
              margin: 0,
            }}
          >
            CyberSquad X
          </h2>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {menuItems.map((item) => {
            const isActive = activeTab === item.name;
            return (
              <div
                key={item.name}
                onClick={() => setActiveTab(item.name)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  padding: "12px 16px",
                  borderRadius: "10px",
                  cursor: "pointer",
                  fontSize: "15px",
                  fontWeight: isActive ? "600" : "400",
                  color: isActive ? "#ffffff" : "#9ca3af",
                  background: isActive
                    ? "rgba(6, 182, 212, 0.15)"
                    : "transparent",
                  border: isActive
                    ? "1px solid rgba(6, 182, 212, 0.3)"
                    : "1px solid transparent",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.color = "#ffffff";
                    e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.color = "#9ca3af";
                    e.currentTarget.style.background = "transparent";
                  }
                }}
              >
                <span style={{ fontSize: "18px" }}>{item.icon}</span>
                <span>{item.name}</span>
              </div>
            );
          })}
        </div>
      </div>

      <div
        onClick={handleLogout}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "12px 16px",
          borderRadius: "10px",
          cursor: "pointer",
          fontSize: "15px",
          color: "#f87171",
          border: "1px solid transparent",
          transition: "all 0.2s ease",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "rgba(239, 68, 68, 0.1)";
          e.currentTarget.style.border = "1px solid rgba(239, 68, 68, 0.2)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.border = "1px solid transparent";
        }}
      >
        <span style={{ fontSize: "18px" }}>🚪</span>
        <span style={{ fontWeight: "600" }}>Disconnect Session</span>
      </div>
    </div>
  );
}

export default Sidebar;