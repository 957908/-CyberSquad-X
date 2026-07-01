class OWASPAgent:

    def map_vulnerabilities(self, vulnerabilities):

        findings = []

        for vuln in vulnerabilities:

            if "Missing Security Headers" in vuln:
                findings.append({
                    "owasp": "A05 Security Misconfiguration",
                    "reason": vuln
                })

            elif "Admin Panel Exposed" in vuln:
                findings.append({
                    "owasp": "A01 Broken Access Control",
                    "reason": vuln
                })

            elif "Dashboard Accessible" in vuln:
                findings.append({
                    "owasp": "A01 Broken Access Control",
                    "reason": vuln
                })

            elif "Login Page Accessible" in vuln:
                findings.append({
                    "owasp": "A07 Identification and Authentication Failures",
                    "reason": vuln
                })

        return findings