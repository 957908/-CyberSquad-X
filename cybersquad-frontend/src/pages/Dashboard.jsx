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

  const [activeSection, setActiveSection] = useState("Dashboard");
  const [sysLoading, setSysLoading] = useState(false);
  const [sysResult, setSysResult] = useState(null);
  const [sysError, setSysError] = useState("");
  const [selectedDevice, setSelectedDevice] = useState("windows"); // "windows" or "android"

  const runSystemScan = async () => {
    setSysLoading(true);
    setSysError("");
    setSysResult(null);
    try {
      const endpoint = selectedDevice === "windows" ? "scan-system" : "scan-android";
      const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      const data = await response.json();
      if (data.success) {
        setSysResult(data);
      } else {
        setSysError(data.error || "An error occurred during system audit.");
      }
    } catch (err) {
      setSysError("Unable to communicate with the scanner API.");
      console.error(err);
    } finally {
      setSysLoading(false);
    }
  };

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
      <Sidebar activeTab={activeSection} setActiveTab={setActiveSection} />
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
          {activeSection === "Dashboard" ? "🛡️ CyberSquad X Security Console" : "💻 Local & Device System Audit"}
        </h1>

      {activeSection === "Dashboard" && (
        <>
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
        </>
      )}

      {activeSection === "System Audit" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "25px", fontFamily: "'Outfit', sans-serif" }}>
          
          {/* Device Selector */}
          <div style={{ display: "flex", gap: "15px", marginBottom: "5px" }}>
            <button
              onClick={() => { setSelectedDevice("windows"); setSysResult(null); setSysError(""); }}
              style={{
                padding: "12px 24px",
                background: selectedDevice === "windows" ? "rgba(6, 182, 212, 0.15)" : "rgba(17, 24, 39, 0.4)",
                border: selectedDevice === "windows" ? "1px solid #06b6d4" : "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "10px",
                color: "white",
                fontWeight: "600",
                fontSize: "15px",
                cursor: "pointer",
                transition: "all 0.2s ease"
              }}
            >
              💻 Local Windows OS Audit
            </button>
            <button
              onClick={() => { setSelectedDevice("android"); setSysResult(null); setSysError(""); }}
              style={{
                padding: "12px 24px",
                background: selectedDevice === "android" ? "rgba(6, 182, 212, 0.15)" : "rgba(17, 24, 39, 0.4)",
                border: selectedDevice === "android" ? "1px solid #06b6d4" : "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "10px",
                color: "white",
                fontWeight: "600",
                fontSize: "15px",
                cursor: "pointer",
                transition: "all 0.2s ease"
              }}
            >
              📱 Connected Android USB (Cable)
            </button>
          </div>

          {/* Scanner Trigger Card */}
          <div style={{
            padding: "25px",
            background: "rgba(17, 25, 40, 0.55)",
            backdropFilter: "blur(12px)",
            borderRadius: "16px",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            display: "flex",
            flexDirection: "column",
            gap: "15px"
          }}>
            <h3 style={{ margin: 0, fontSize: "18px", fontWeight: "700", color: "#22d3ee" }}>
              {selectedDevice === "windows" ? "Local PC Security Scan" : "Mobile Security Audit (via USB Cable)"}
            </h3>
            <p style={{ margin: 0, color: "#9ca3af", fontSize: "14px", lineHeight: "1.6" }}>
              {selectedDevice === "windows" 
                ? "Analyzes local system properties including Windows Defender active protection, active Firewall profiles (Domain/Private/Public), system listening TCP ports, and installed OS hotfixes."
                : "Queries your connected Android device over ADB cable link. Please ensure your device is connected via USB, developer options is enabled, and USB debugging is turned on."
              }
            </p>
            <button
              onClick={runSystemScan}
              disabled={sysLoading}
              style={{
                padding: "12px 24px",
                background: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                border: "none",
                borderRadius: "8px",
                color: "white",
                fontWeight: "700",
                fontSize: "15px",
                cursor: "pointer",
                width: "fit-content",
                boxShadow: "0 0 16px rgba(6, 182, 212, 0.25)",
                transition: "all 0.2s ease",
                opacity: sysLoading ? 0.6 : 1
              }}
            >
              {sysLoading ? "⚡ Querying System..." : "⚡ Run Diagnostics Audit"}
            </button>
          </div>

          {/* Loading State */}
          {sysLoading && (
            <div style={{ textAlign: "center", padding: "40px 0" }}>
              <div className="loader" style={{ border: "4px solid rgba(255, 255, 255, 0.1)", borderTop: "4px solid #06b6d4", borderRadius: "50%", width: "40px", height: "40px", animation: "spin 1s linear infinite", margin: "0 auto 15px" }} />
              <p style={{ color: "#9ca3af", fontSize: "15px" }}>Performing deep security analysis. Please wait...</p>
            </div>
          )}

          {/* Error State */}
          {sysError && (
            <div style={{
              padding: "20px",
              background: "rgba(239, 68, 68, 0.1)",
              border: "1px solid rgba(239, 68, 68, 0.2)",
              borderRadius: "12px",
              color: "#fca5a5"
            }}>
              <h4 style={{ margin: "0 0 8px", fontSize: "16px", fontWeight: "700" }}>⚠️ Audit Failed</h4>
              <p style={{ margin: 0, fontSize: "14px", lineHeight: "1.5" }}>{sysError}</p>
            </div>
          )}

          {/* Results State */}
          {sysResult && (
            <div style={{ display: "flex", flexDirection: "column", gap: "25px" }}>
              
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "25px" }}>
                
                {/* Left Panel: Raw Scan Metrics */}
                <div style={{
                  padding: "25px",
                  background: "rgba(17, 25, 40, 0.55)",
                  backdropFilter: "blur(12px)",
                  borderRadius: "16px",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                  display: "flex",
                  flexDirection: "column",
                  gap: "20px"
                }}>
                  <h3 style={{ margin: 0, fontSize: "18px", fontWeight: "700", borderBottom: "1px solid rgba(255, 255, 255, 0.1)", paddingBottom: "10px" }}>
                    🔍 Telemetry Report
                  </h3>

                  {selectedDevice === "windows" ? (
                    <>
                      {/* OS Version */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Operating System</span>
                        <div style={{ fontSize: "16px", fontWeight: "600", marginTop: "4px" }}>{sysResult.report.os_version}</div>
                      </div>

                      {/* Windows Defender */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Windows Defender Status</span>
                        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", marginTop: "6px" }}>
                          <span style={{ padding: "4px 10px", borderRadius: "20px", fontSize: "12px", background: sysResult.report.defender?.AntivirusEnabled ? "rgba(34, 197, 94, 0.15)" : "rgba(239, 68, 68, 0.15)", color: sysResult.report.defender?.AntivirusEnabled ? "#4ade80" : "#f87171", border: sysResult.report.defender?.AntivirusEnabled ? "1px solid rgba(34, 197, 94, 0.3)" : "1px solid rgba(239, 68, 68, 0.3)" }}>
                            Antivirus: {sysResult.report.defender?.AntivirusEnabled ? "ACTIVE" : "INACTIVE"}
                          </span>
                          <span style={{ padding: "4px 10px", borderRadius: "20px", fontSize: "12px", background: sysResult.report.defender?.RealTimeProtectionEnabled ? "rgba(34, 197, 94, 0.15)" : "rgba(239, 68, 68, 0.15)", color: sysResult.report.defender?.RealTimeProtectionEnabled ? "#4ade80" : "#f87171", border: sysResult.report.defender?.RealTimeProtectionEnabled ? "1px solid rgba(34, 197, 94, 0.3)" : "1px solid rgba(239, 68, 68, 0.3)" }}>
                            Real-Time Guard: {sysResult.report.defender?.RealTimeProtectionEnabled ? "ACTIVE" : "INACTIVE"}
                          </span>
                        </div>
                      </div>

                      {/* Firewalls */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Active Firewall Profiles</span>
                        <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginTop: "8px" }}>
                          {Array.isArray(sysResult.report.firewall) ? sysResult.report.firewall.map(fw => (
                            <div key={fw.Name} style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", fontSize: "13px" }}>
                              <span>{fw.Name} Profile</span>
                              <span style={{ color: fw.Enabled ? "#4ade80" : "#f87171", fontWeight: "bold" }}>
                                {fw.Enabled ? "ENABLED" : "DISABLED"}
                              </span>
                            </div>
                          )) : <div style={{ fontSize: "13px", color: "#f87171" }}>Unable to read firewall status</div>}
                        </div>
                      </div>

                      {/* Active Listener Ports */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Exposed Listener TCP Ports ({sysResult.report.open_ports?.length || 0})</span>
                        <div style={{ maxHeight: "150px", overflowY: "auto", marginTop: "8px", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "8px" }}>
                          {sysResult.report.open_ports?.length > 0 ? (
                            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "12px", textAlign: "left" }}>
                              <thead>
                                <tr style={{ background: "rgba(255, 255, 255, 0.05)", borderBottom: "1px solid rgba(255, 255, 255, 0.08)" }}>
                                  <th style={{ padding: "8px" }}>Local Address</th>
                                  <th style={{ padding: "8px" }}>Port</th>
                                </tr>
                              </thead>
                              <tbody>
                                {sysResult.report.open_ports.map((port, index) => (
                                  <tr key={index} style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.03)" }}>
                                    <td style={{ padding: "8px" }}>{port.LocalAddress || "0.0.0.0"}</td>
                                    <td style={{ padding: "8px", color: "#22d3ee", fontWeight: "600" }}>{port.LocalPort}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          ) : (
                            <div style={{ padding: "12px", fontSize: "13px", textAlign: "center", color: "#9ca3af" }}>No active listener ports found</div>
                          )}
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      {/* Android Device Identity */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Device Identity</span>
                        <div style={{ fontSize: "16px", fontWeight: "600", marginTop: "4px" }}>
                          {sysResult.report.device_info?.brand} {sysResult.report.device_info?.model}
                        </div>
                      </div>

                      {/* OS Details */}
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
                        <div>
                          <span style={{ color: "#9ca3af", fontSize: "13px" }}>Android Version</span>
                          <div style={{ fontSize: "15px", fontWeight: "600", marginTop: "4px" }}>v{sysResult.report.device_info?.android_version}</div>
                        </div>
                        <div>
                          <span style={{ color: "#9ca3af", fontSize: "13px" }}>Security Patch Level</span>
                          <div style={{ fontSize: "15px", fontWeight: "600", marginTop: "4px", color: "#38bdf8" }}>{sysResult.report.device_info?.security_patch}</div>
                        </div>
                      </div>

                      {/* Device Security Configuration */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Vulnerability Configuration Checks</span>
                        <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginTop: "8px" }}>
                          <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", fontSize: "13px" }}>
                            <span>USB Debugging (ADB Link)</span>
                            <span style={{ color: sysResult.report.security_config?.usb_debugging ? "#f87171" : "#4ade80", fontWeight: "bold" }}>
                              {sysResult.report.security_config?.usb_debugging ? "ENABLED (Vulnerable)" : "DISABLED (Secure)"}
                            </span>
                          </div>
                          <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", fontSize: "13px" }}>
                             <span>Install from Unknown Sources</span>
                             <span style={{ color: sysResult.report.security_config?.install_non_market_apps ? "#f87171" : "#4ade80", fontWeight: "bold" }}>
                               {sysResult.report.security_config?.install_non_market_apps ? "ALLOWED (Risk)" : "BLOCKED (Secure)"}
                             </span>
                           </div>
                           <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 12px", background: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", fontSize: "13px" }}>
                             <span>Mock Locations Enabled</span>
                             <span style={{ color: sysResult.report.security_config?.mock_locations ? "#f87171" : "#4ade80", fontWeight: "bold" }}>
                               {sysResult.report.security_config?.mock_locations ? "ACTIVE (Risk)" : "INACTIVE (Secure)"}
                             </span>
                           </div>
                        </div>
                      </div>

                      {/* Third Party Packages */}
                      <div>
                        <span style={{ color: "#9ca3af", fontSize: "13px" }}>Installed User Apps ({sysResult.report.third_party_apps?.count || 0})</span>
                        <div style={{ maxHeight: "150px", overflowY: "auto", marginTop: "8px", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "8px", padding: "10px", fontSize: "12px", background: "rgba(255, 255, 255, 0.01)" }}>
                          {sysResult.report.third_party_apps?.list?.length > 0 ? (
                            sysResult.report.third_party_apps.list.map((pkg, idx) => (
                              <div key={idx} style={{ padding: "4px 0", color: "#9ca3af", textOverflow: "ellipsis", overflow: "hidden", whiteSpace: "nowrap" }}>
                                • {pkg}
                              </div>
                            ))
                          ) : (
                            <div style={{ color: "#9ca3af", textAlign: "center" }}>No third-party packages found</div>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>

                {/* Right Panel: AI Analysis Advice */}
                <div style={{
                  padding: "25px",
                  background: "rgba(17, 25, 40, 0.55)",
                  backdropFilter: "blur(12px)",
                  borderRadius: "16px",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                  display: "flex",
                  flexDirection: "column",
                  gap: "15px"
                }}>
                  <h3 style={{ margin: 0, fontSize: "18px", fontWeight: "700", color: "#38bdf8", borderBottom: "1px solid rgba(255, 255, 255, 0.1)", paddingBottom: "10px" }}>
                    🧠 AI Analyst Security Advisory
                  </h3>
                  <div style={{
                    fontSize: "14px",
                    lineHeight: "1.6",
                    color: "#d1d5db",
                    overflowY: "auto",
                    maxHeight: "450px",
                    paddingRight: "10px"
                  }}>
                    {sysResult.analysis?.split("\n").map((line, idx) => {
                      if (line.startsWith("###")) {
                        return <h4 key={idx} style={{ color: "#22d3ee", margin: "18px 0 8px", fontSize: "16px", fontWeight: "700" }}>{line.replace("###", "").trim()}</h4>;
                      }
                      if (line.startsWith("-") || line.startsWith("•")) {
                        return <p key={idx} style={{ margin: "4px 0 4px 12px", textIndent: "-12px" }}>• {line.substring(1).trim()}</p>;
                      }
                      if (line.trim() === "") return <div key={idx} style={{ height: "8px" }} />;
                      return <p key={idx} style={{ margin: "0 0 10px" }}>{line}</p>;
                    })}
                  </div>
                </div>

              </div>

            </div>
          )}

        </div>
      )}
      </div>
    </div>
  );
}
export default Dashboard;