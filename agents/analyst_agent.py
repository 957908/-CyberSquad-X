class AnalystAgent:

    def analyze(self, scan_result):

        findings = []

        if "22/tcp" in scan_result:
            findings.append("""
SSH Port (22) Found

Risk:
Brute Force Attacks

Recommendation:
- Disable root login
- Use SSH keys
- Enable MFA
""")

        if "80/tcp" in scan_result:
            findings.append("""
HTTP Port (80) Found

Risk:
Web Application Attacks

Recommendation:
- Use HTTPS
- Update Apache
- Apply Security Headers
""")

        if "Apache" in scan_result:
            findings.append("""
Apache Web Server Detected

Recommendation:
- Check CVEs
- Update to latest version
- Disable unused modules
""")

        if "Linux" in scan_result:
            findings.append("""
Linux Operating System Detected

Recommendation:
- Apply security patches
- Harden SSH configuration
- Monitor logs
""")

        return "\n".join(findings)