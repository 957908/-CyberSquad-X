function HistoryTable({ history }) {
  return (
    <div
      className="panel"
      style={{
        marginTop: "20px",
      }}
    >
      <h2>📜 Scan History</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "10px",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Target</th>
            <th>Risk</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {history?.map((scan) => (
            <tr key={scan[0]}>
              <td>{scan[0]}</td>

              <td>{scan[1]}</td>

              <td
                style={{
                  color:
                    scan[2] >= 70
                      ? "#ef4444"
                      : scan[2] >= 40
                      ? "#f59e0b"
                      : "#22c55e",
                  fontWeight: "bold",
                }}
              >
                {scan[2]}
              </td>

              <td>
                {new Date(scan[3]).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;