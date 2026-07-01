function StatsCards({
  riskScore,
  vulnerabilities,
  openPorts,
}) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit,minmax(220px,1fr))",
        gap: "20px",
        marginTop: "20px",
      }}
    >
      <div className="card">
        <h3>🛡 Risk Score</h3>
        <h1>{riskScore}</h1>
      </div>

      <div className="card">
        <h3>⚠ Vulnerabilities</h3>
        <h1>{vulnerabilities}</h1>
      </div>

      <div className="card">
        <h3>🌐 Open Ports</h3>
        <h1>{openPorts}</h1>
      </div>
    </div>
  );
}

export default StatsCards;