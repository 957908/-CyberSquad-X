class CVEAgent:

    def search_vulnerabilities(self, scan_result):

        vulnerabilities = []

        if "OpenSSH" in scan_result:

            vulnerabilities.append({
                "service": "OpenSSH",
                "risk": "High",
                "recommendation": "Upgrade OpenSSH"
            })

        if "Apache" in scan_result:

            vulnerabilities.append({
                "service": "Apache",
                "risk": "Critical",
                "recommendation": "Update Apache Server"
            })

        return vulnerabilities