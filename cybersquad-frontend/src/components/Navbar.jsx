import { useState, useEffect } from "react";

function Navbar() {
  const userRole = localStorage.getItem("role") || "analyst";
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "dark");

  useEffect(() => {
    if (theme === "light") {
      document.body.classList.add("light-theme");
    } else {
      document.body.classList.remove("light-theme");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div
      style={{
        background: "var(--bg-panel)",
        backdropFilter: "blur(8px)",
        padding: "16px 24px",
        borderRadius: "12px",
        marginBottom: "30px",
        border: "1px solid var(--border-color)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 4px 20px var(--shadow-color)",
        fontFamily: "'Outfit', sans-serif",
      }}
    >
      <h2
        style={{
          margin: 0,
          fontSize: "18px",
          fontWeight: "600",
          color: "var(--accent-cyan)",
          display: "flex",
          alignItems: "center",
          gap: "8px",
        }}
      >
        <span
          style={{
            display: "inline-block",
            width: "8px",
            height: "8px",
            background: "#22c55e",
            borderRadius: "50%",
            boxShadow: "0 0 10px #22c55e",
          }}
        ></span>
        Security Operations Center
      </h2>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "15px",
          fontSize: "14px",
        }}
      >
        <span style={{ color: "var(--text-gray)" }}>
          Role:{" "}
          <strong style={{ color: "var(--accent-cyan)", textTransform: "uppercase" }}>
            {userRole}
          </strong>
        </span>
        <span
          style={{
            background: "rgba(34, 197, 94, 0.1)",
            color: "#22c55e",
            padding: "4px 10px",
            borderRadius: "6px",
            fontWeight: "600",
            border: "1px solid rgba(34, 197, 94, 0.2)",
          }}
        >
          Secure Node
        </span>
        <button
          onClick={toggleTheme}
          style={{
            background: "rgba(255, 255, 255, 0.05)",
            border: "1px solid var(--border-color)",
            borderRadius: "6px",
            padding: "5px 10px",
            color: "var(--text-white)",
            cursor: "pointer",
            fontSize: "14px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transition: "all 0.2s ease"
          }}
        >
          {theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>
    </div>
  );
}

export default Navbar;