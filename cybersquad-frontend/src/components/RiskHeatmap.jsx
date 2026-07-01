import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

function RiskHeatmap({ history }) {

  const data = [
    {
      level: "Low",
      value: history.filter(
        x => x[2] < 40
      ).length,
    },
    {
      level: "Medium",
      value: history.filter(
        x => x[2] >= 40 &&
             x[2] < 70
      ).length,
    },
    {
      level: "High",
      value: history.filter(
        x => x[2] >= 70
      ).length,
    },
  ];

  return (
    <div
      className="panel"
      style={{
        marginTop: "20px",
      }}
    >
      <h2>
        🔥 Risk Distribution
      </h2>

      <BarChart
        width={600}
        height={300}
        data={data}
      >
        <CartesianGrid />

        <XAxis
          dataKey="level"
        />

        <YAxis />

        <Tooltip />

        <Bar
          dataKey="value"
          fill="#06b6d4"
        />
      </BarChart>
    </div>
  );
}

export default RiskHeatmap;