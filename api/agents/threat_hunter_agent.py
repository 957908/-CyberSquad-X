class ThreatHunterAgent:

    def hunt(
        self,
        vulnerabilities,
        cve,
        ports
    ):

        threats = []

        # Admin Panel
        if (
            "Admin Panel Exposed"
            in vulnerabilities
        ):

            threats.append({
                "threat":
                "Privilege Escalation",

                "severity":
                "High"
            })

        # Login
        if (
            "Login Page Accessible"
            in vulnerabilities
        ):

            threats.append({
                "threat":
                "Credential Stuffing",

                "severity":
                "Medium"
            })

        # Critical CVEs
        for item in cve:

            if (
                item.get(
                    "severity"
                )
                ==
                "Critical"
            ):

                threats.append({
                    "threat":
                    "Remote Code Execution",

                    "severity":
                    "Critical"
                })

        # Ports
        for port in ports:

            if (
                port.get(
                    "port"
                )
                ==
                "445/tcp"
            ):

                threats.append({
                    "threat":
                    "SMB Exploitation",

                    "severity":
                    "Critical"
                })

            if (
                port.get(
                    "port"
                )
                ==
                "3389/tcp"
            ):

                threats.append({
                    "threat":
                    "RDP Brute Force",

                    "severity":
                    "High"
                })

        return threats