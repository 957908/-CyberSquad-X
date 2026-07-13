import { useState, useEffect } from "react";
import { API_BASE_URL } from "../services/api";
import LiveThreatCard from "../components/LiveThreatCard";

import RiskCard from "../components/RiskCard";
import RiskBarChart from "../components/BarChart";
import VulnerabilityPieChart from "../components/VulnerabilityPieChart";
import HistoryTable from "../components/HistoryTable";
import StatsCards from "../components/StatsCards";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import RiskHeatmap from "../components/RiskHeatmap";
import { generatePDF } from "../utils/pdfReport";
import CVSSChart from "../components/CVSSChart";

function Dashboard() {
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [progress, setProgress] = useState(0);

  const loadHistory = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/history`
      );

      const data = await response.json();

      setHistory(data.history);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);


  const startScan = async () => {
    try {
      setLoading(true);
      setProgress(10);

      const response = await fetch(
        `${API_BASE_URL}/scan`,
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
      setProgress(80);

      const data = await response.json();
      setProgress(100);

      console.log(data);
      console.log("History:", history);


      setResult(data);

      loadHistory();
    } catch (error) {
      console.error(error);
      alert(error.message);
    } finally {
      setLoading(false);
      setProgress(0);

    }
  };

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        backgroundColor: "#0b0f19",
        color: "white",
        fontFamily: "'Outfit', 'Inter', sans-serif",
      }}
    >
      <Sidebar />
      <div
        style={{
          marginLeft: "250px",
          flex: 1,
          padding: "30px",
          boxSizing: "border-box",
          minWidth: 0,
        }}
      >
        <Navbar />

        <h1
          style={{
            marginBottom: "25px",
            fontSize: "40px",
            fontWeight: "700",
            background: "linear-gradient(135deg, #ffffff 0%, #a5f3fc 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          🛡️ CyberSquad X Security Console
        </h1>

      <div
        style={{
          display: "flex",
          gap: "12px",
          marginBottom: "30px",
          background: "rgba(17, 24, 39, 0.4)",
          padding: "20px",
          borderRadius: "12px",
          border: "1px solid rgba(6, 182, 212, 0.1)",
          alignItems: "center",
        }}
      >
        <input
          value={target}
          onChange={(e) =>
            setTarget(e.target.value)
          }
          placeholder="https://www.target-domain.com"
          style={{
            padding: "14px 20px",
            width: "100%",
            maxWidth: "500px",
            fontSize: "16px",
          }}
        />

        <button
          onClick={startScan}
          style={{
            padding: "14px 28px",
            fontSize: "16px",
          }}
        >
          ⚡ Initiate Audit
        </button>
      </div>
        {loading && (
        <>
            <h3>🔍 Scanning Target...</h3>

            <div
            style={{
                width: "100%",
                height: "20px",
                background: "#334155",
                borderRadius: "10px",
                overflow: "hidden",
                marginBottom: "20px",
            }}
            >
            <div
                style={{
                width: `${progress}%`,
                height: "100%",
                background: "#06b6d4",
                transition: "0.5s",
                }}
            />
            </div>
        </>
        )}
            {result && (
        <>
          <StatsCards
            riskScore={result.risk_score}
            vulnerabilities={
              result.vulnerabilities?.length || 0
            }
            openPorts={
              result.nmap_scan
                ?.match(/\d+\/tcp/g)
                ?.length || 0
            }
          />
          <LiveThreatCard
            score={result.risk_score}
          />

          <RiskCard
            score={result.risk_score}
          />

          <RiskBarChart
            score={result.risk_score}
          />
          <RiskHeatmap
            history={history}
          />

          <VulnerabilityPieChart
            vulnerabilities={
              result.vulnerabilities
            }
          />
          <CVSSChart
            cve={result.cve || []}
          />

          <div className="panel">
            <h2>⚠ Vulnerabilities</h2>

            {result.vulnerabilities?.length >
            0 ? (
              result.vulnerabilities.map(
                (vuln, index) => (
                  <p key={index}>
                    ⚠️ {vuln}
                  </p>
                )
              )
            ) : (
              <p>
                ✅ No vulnerabilities
                detected
              </p>
            )}
          </div>

          <div className="panel">
            <h2>🤖 AI Analysis</h2>

            <pre>
              {result.ai_analysis}
            </pre>
          </div>
          <div className="panel">
            <h2>
              🛡 Security Header Grade
            </h2>

            <h1
              style={{
                fontSize: "60px",
                color:
                  result.security_grade
                    ?.grade === "A+"
                    ? "#22c55e"
                    : result.security_grade
                        ?.grade === "F"
                    ? "#ef4444"
                    : "#f59e0b",
              }}
            >
              {
                result.security_grade
                  ?.grade
              }
            </h1>

            <p>
              Score:
              {
                result.security_grade
                  ?.score
              }
              /100
            </p>

            <h3>
              Missing Headers
            </h3>

            {result.security_grade
              ?.missing_headers
              ?.map(
                (header, index) => (
                  <p key={index}>
                    ❌ {header}
                  </p>
                )
              )}
          </div>

    <div className="panel">
        <h2>🌍 WHOIS Information</h2>

        <pre
            style={{
            whiteSpace: "pre-wrap",
            color: "#38bdf8",
            }}
        >
            {JSON.stringify(
            result.whois,
            null,
            2
            )}
        </pre>
        </div>

        <div
        className="panel"
        style={{
            marginTop: "20px",
        }}
        >
        <h2>🔒 SSL Information</h2>

        <p>
            Status:
            {result.ssl_scan?.ssl_enabled
            ? " ✅ Secure"
            : " ❌ Not Secure"}
        </p>

        <p>
            TLS Version:
            {result.ssl_scan?.tls_version}
        </p>

        <p>
            Days Remaining:
            {result.ssl_scan?.days_remaining}
        </p>

        <pre
            style={{
            whiteSpace: "pre-wrap",
            color: "#22c55e",
            }}
        >
            {JSON.stringify(
            result.ssl_scan,
            null,
            2
            )}
        </pre>
        </div>
        <div className="panel">
        <h2>🌍 GeoIP Information</h2>

        <p>
            Country:
            {result.geoip?.country}
        </p>

        <p>
            City:
            {result.geoip?.city}
        </p>

        <p>
            ISP:
            {result.geoip?.isp}
        </p>

        <p>
            Latitude:
            {result.geoip?.lat}
        </p>

        <p>
            Longitude:
            {result.geoip?.lon}
        </p>
        </div>
        <div className="panel">
        <h2>🚨 CVE Detection</h2>

        {result.cve_scan?.length > 0 ? (
            result.cve_scan.map(
            (cve, index) => (
                <div
                key={index}
                style={{
                    marginBottom: "15px",
                    padding: "10px",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                }}
                >
                <p>
                    Service:
                    {cve.service}
                </p>

                <p>
                    CVE:
                    {cve.cve}
                </p>

                <p>
                    CVSS:
                    {cve.cvss}
                </p>

                <p>
                    Severity:
                    {cve.severity}
                </p>
                </div>
            )
            )
        ) : (
            <p>
            ✅ No known CVEs found
            </p>
        )}
        </div>
        <div className="panel">
        <h2>🛡 OWASP Top 10 Mapping</h2>

        {result.owasp_scan?.length > 0 ? (
            result.owasp_scan.map(
            (item, index) => (
                <div
                key={index}
                style={{
                    marginBottom: "15px",
                    padding: "12px",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                }}
                >
                <p>
                    <strong>
                    {item.owasp}
                    </strong>
                </p>

                <p>
                    {item.reason}
                </p>
                </div>
            )
            )
        ) : (
            <p>
            ✅ No OWASP Issues Found
            </p>
        )}
        </div>

        <div className="panel">
        <h2>🌐 Nmap Scan Result</h2>
        
        <pre
            style={{
            whiteSpace: "pre-wrap",
            color: "#38bdf8",
            }}
        >
            {result.nmap_scan}
        </pre>
        </div>

        <div className="panel">
        <h2>🌐 Subdomain Scan Result</h2>

        {result.subdomain_scan?.length > 0 ? (
            result.subdomain_scan.map(
            (subdomain, index) => (
                <div
                key={index}
                style={{
                    marginBottom: "15px",
                    padding: "10px",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                }}
                >
                <p>
                    Subdomain:
                    {subdomain.subdomain}
                </p>

                <p>
                    Status:
                    {subdomain.status}
                </p>
                </div>
            )
            )
        ) : (
            <p>
            ✅ No subdomains found
            </p>
        )}
        </div>
        <div className="panel">
          <h2>
            🎯 MITRE ATT&CK
          </h2>

          {result.mitre?.map(
            (m, i) => (
              <p key={i}>
                {m.technique}
                {" - "}
                {m.name}
              </p>
            )
          )}
        </div>
        <div className="panel">
          <h2>
            🎯 Attack Surface
          </h2>

          <p>
            Subdomains:
            {
              result.attack_surface
                ?.subdomains_count
            }
          </p>

          <p>
            Risk Level:
            {
              result.attack_surface
                ?.risk_level
            }
          </p>

          <h3>
            Open Ports
          </h3>

          {result.attack_surface
            ?.open_ports
            ?.map(
              (port, index) => (
                <p key={index}>
                  {port}
                </p>
              )
            )}
        </div>
        <div className="panel">
  <h2>
    🚨 Threat Hunting
          </h2>

          {result.threat_hunting
            ?.length > 0 ? (

            result.threat_hunting.map(
              (t, index) => (
                <div
                  key={index}
                  style={{
                    marginBottom:
                      "10px",
                  }}
                >
                  <p>
                    Threat:
                    {t.threat}
                  </p>

                  <p
                    style={{
                      color:
                        t.severity
                        ===
                        "Critical"
                        ? "#ef4444"
                        : "#f59e0b",
                    }}
                  >
                    Severity:
                    {t.severity}
                  </p>
                </div>
              )
            )

          ) : (
            <p>
              No active
              threats found
            </p>
          )}
        </div>
        <div className="panel">
            <h2>
              👨‍💻 Security Analyst
            </h2>

            {result.security_analysis?.map(
              (item, index) => (
                <p key={index}>
                  🔹 {item}
                </p>
              )
            )}
          </div>
          <div className="panel">
            <h2>
              📋 Compliance Audit
            </h2>

            {result.compliance?.length > 0 ? (

              result.compliance.map(
                (item, index) => (
                  <div
                    key={index}
                    style={{
                      marginBottom: "15px",
                    }}
                  >
                    <p>
                      Framework:
                      {item.framework}
                    </p>

                    <p
                      style={{
                        color:
                          item.status ===
                          "Failed"
                          ||
                          item.status ===
                          "Non-Compliant"
                          ? "#ef4444"
                          : "#f59e0b",
                      }}
                    >
                      Status:
                      {item.status}
                    </p>

                    <p>
                      Reason:
                      {item.reason}
                    </p>
                  </div>
                )
              )

            ) : (
              <p>
                ✅ Fully Compliant
              </p>
            )}
          </div>
          <div className="panel">
          <h2>
            🚑 Incident Response
          </h2>

          {result.incident_response
            ?.map(
              (item, index) => (
                <div
                  key={index}
                  style={{
                    marginBottom:
                      "10px",
                  }}
                >
                  <p>
                    Priority:
                    {item.priority}
                  </p>

                  <p>
                    Action:
                    {item.action}
                  </p>
                </div>
              )
            )}
        </div>
        <div className="panel">
            <h2>
              🛠 Technology Stack
            </h2>

            {result.technologies?.length > 0 ? (
              result.technologies.map(
                (tech, index) => (
                  <p key={index}>
                    ✅ {tech}
                  </p>
                )
              )
            ) : (
              <p>
                No technologies found
              </p>
            )}
          </div>
          <div className="panel">
              <h2>
                🔌 Port Intelligence
              </h2>

              {result.port_intelligence?.map(
                (port, index) => (
                  <div
                    key={index}
                    style={{
                      padding: "10px",
                      marginBottom: "10px",
                      border: "1px solid #334155",
                      borderRadius: "8px",
                    }}
                  >
                    <p>
                      Port:
                      {port.port}
                    </p>

                    <p>
                      Service:
                      {port.service}
                    </p>

                    <p>
                      State:
                      {port.state}
                    </p>

                    <p
                      style={{
                        color:
                          port.severity === "Critical"
                            ? "#ef4444"
                            : port.severity === "High"
                            ? "#f97316"
                            : "#22c55e",
                      }}
                    >
                      Severity:
                      {port.severity}
                    </p>
                  </div>
                )
              )}
            </div>
            <div className="panel">
                <h2>
                  📄 Executive Report
                </h2>

                {result.executive_report?.map(
                  (line, index) => (
                    <p key={index}>
                      • {line}
                    </p>
                  )
                )}
              </div>
                    <a
          href={
            `${API_BASE_URL}/`
            + result.pdf_report
          }
          target="_blank"
        >
          <button>
            📄 Executive Report
          </button>
        </a>

          <HistoryTable
            history={history}
          />

          <button
            onClick={() =>
              generatePDF(result)
            }
            style={{
              marginTop: "20px",
              padding: "14px 25px",
              background: "#22c55e",
              border: "none",
              borderRadius: "8px",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            📄 Download PDF Report
          </button>
        </>
      )}
      </div>
    </div>
  );
}
export default Dashboard;