class IncidentResponseAgent:

    def respond(
        self,
        threats,
        vulnerabilities
    ):

        actions = []

        for threat in threats:

            if threat["severity"] == "Critical":

                actions.append({
                    "priority":
                    "P1",

                    "action":
                    "Immediate incident response required"
                })

        for vuln in vulnerabilities:

            if (
                "Admin Panel"
                in vuln
            ):

                actions.append({
                    "priority":
                    "P2",

                    "action":
                    "Restrict admin access using VPN/IP whitelist"
                })

            if (
                "Login"
                in vuln
            ):

                actions.append({
                    "priority":
                    "P2",

                    "action":
                    "Enable MFA and rate limiting"
                })

            if (
                "Headers"
                in vuln
            ):

                actions.append({
                    "priority":
                    "P3",

                    "action":
                    "Implement missing security headers"
                })

        return actions