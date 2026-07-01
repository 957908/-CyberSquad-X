function RiskCard({ score }) {
  let color = "#22c55e";

  if (score > 70) {
    color = "#ef4444";
  } else if (score > 40) {
    color = "#f59e0b";
  }

  return (
    <div
      style={{
        background: "#1e293b",
        padding: "20px",
        borderRadius: "10px",
        marginTop: "20px",
      }}
    >
      <h2>Risk Score</h2>

      <h1
        style={{
          color: color,
          fontSize: "48px",
        }}
      >
        {score}/100
      </h1>
    </div>
  );
}

export default RiskCard;