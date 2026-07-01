import { useState } from "react";

function Scan() {
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);

  const startScan = async () => {
    const response = await fetch(
      "http://127.0.0.1:8000/scan",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          target,
        }),
      }
    );

    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>🛡 CyberSquad X</h1>

      <input
        type="text"
        placeholder="https://www.cdac.in"
        value={target}
        onChange={(e) =>
          setTarget(e.target.value)
        }
      />

      <button onClick={startScan}>
        Scan Target
      </button>

      {result && (
        <pre>
          {JSON.stringify(
            result,
            null,
            2
          )}
        </pre>
      )}
    </div>
  );
}
const data = await response.json();

console.log(data);

setResult(data);
{result && (
  <div>
    <h2>Scan Result</h2>

    <p>
      Risk Score:
      {result.risk_score}
    </p>

    <pre>
      {JSON.stringify(
        result,
        null,
        2
      )}
    </pre>
  </div>
)}
export default Scan;