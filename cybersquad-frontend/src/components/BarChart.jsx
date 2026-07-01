import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function RiskBarChart({ score }) {
  const data = [
    {
      name: "Risk Score",
      value: score,
    },
  ];

  return (
    <div
      style={{
        background: "#1e293b",
        marginTop: "20px",
        padding: "20px",
        borderRadius: "12px",
      }}
    >
      <h2>📊 Risk Score Chart</h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="name" />

          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Bar
            dataKey="value"
            fill="#06b6d4"
            radius={[10, 10, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RiskBarChart;