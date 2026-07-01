function LiveThreatCard({ score }) {
  let status = "SAFE";
  let color = "#22c55e";

  if (score >= 70) {
    status = "CRITICAL";
    color = "#ef4444";
  } else if (score >= 40) {
    status = "WARNING";
    color = "#f59e0b";
  }

  return (
    <div
      className="panel"
      style={{
        marginTop: "20px",
        textAlign: "center",
      }}
    >
      <h2>🚨 Threat Level</h2>

      <h1
        style={{
          color: color,
          fontSize: "42px",
        }}
      >
        {status}
      </h1>
    </div>
  );
}

export default LiveThreatCard;