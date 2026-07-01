import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from "recharts";

function CVSSChart({ cve }) {

  const critical =
    cve.filter(
      x =>
        x.severity ===
        "Critical"
    ).length;

  const high =
    cve.filter(
      x =>
        x.severity ===
        "High"
    ).length;

  const medium =
    cve.filter(
      x =>
        x.severity ===
        "Medium"
    ).length;

  const data = [
    {
      name: "Critical",
      value: critical,
    },
    {
      name: "High",
      value: high,
    },
    {
      name: "Medium",
      value: medium,
    },
  ];

  return (
    <div className="panel">
      <h2>
        🚨 CVSS Analytics
      </h2>

      <PieChart
        width={400}
        height={300}
      >
        <Pie
          data={data}
          dataKey="value"
          outerRadius={100}
          label
        />

        <Tooltip />
      </PieChart>
    </div>
  );
}

export default CVSSChart;