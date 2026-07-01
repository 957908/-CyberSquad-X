function Navbar() {
  const userRole = localStorage.getItem("role") || "analyst";

  return (
    <div
      style={{
        background: "rgba(17, 24, 39, 0.4)",
        backdropFilter: "blur(8px)",
        padding: "16px 24px",
        borderRadius: "12px",
        marginBottom: "30px",
        border: "1px solid rgba(6, 182, 212, 0.15)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 4px 20px rgba(0, 0, 0, 0.2)",
        fontFamily: "'Outfit', sans-serif",
      }}
    >
      <h2
        style={{
          margin: 0,
          fontSize: "18px",
          fontWeight: "600",
          color: "#06b6d4",
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
        <span style={{ color: "#9ca3af" }}>
          Role:{" "}
          <strong style={{ color: "#06b6d4", textTransform: "uppercase" }}>
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
      </div>
    </div>
  );
}

export default Navbar;