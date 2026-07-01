class PortIntelligenceAgent:

    def analyze(self, nmap_result):

        findings = []

        for line in nmap_result.split("\n"):

            if "/tcp" not in line:
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            port = parts[0]
            state = parts[1]
            service = parts[2]

            severity = "Low"

            if port.startswith("21"):
                severity = "Medium"

            elif port.startswith("22"):
                severity = "Low"

            elif port.startswith("23"):
                severity = "Critical"

            elif port.startswith("445"):
                severity = "Critical"

            elif port.startswith("3389"):
                severity = "High"

            findings.append({
                "port": port,
                "state": state,
                "service": service,
                "severity": severity
            })

        return findings